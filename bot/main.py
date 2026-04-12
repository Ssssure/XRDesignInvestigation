import os
import json
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from openai import OpenAI

from github_ops import commit_article, get_article_content

logging.basicConfig(
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPO = os.environ.get("GITHUB_REPO", "Ssssure/claude-XR-knowledge-base")
MODEL = os.environ.get("MODEL", "anthropic/claude-sonnet-4.6")
ALLOWED_USERS = [
    uid.strip()
    for uid in os.environ.get("ALLOWED_TELEGRAM_USERS", "").split(",")
    if uid.strip()
]

MAX_HISTORY = 60

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# {chat_id: [message_dicts]}
sessions: dict[int, list[dict]] = {}

SYSTEM_PROMPT = f"""\
你是一个帮助用户将主题转化为 GitHub 文章的 AI 助手。
目标仓库：{GITHUB_REPO}

## 沟通风格（即时消息）
- 保持回复简短：几句话或简洁的要点列表，除非用户要求展开。
- 发现阶段每条消息只问一个问题。
- 文章生成后，若用户一条消息有多个问题可一起回答。

## 会话流程

1. **主题接收** — 用户给出主题后，不要直接写文章，先进入发现阶段。

2. **发现（每次一个问题）**
   每次只问最重要的未知维度：
   - 目标：科普、教学、决策、记录研究…
   - 受众：角色、经验水平
   - 范围：必含要点、排除项、篇幅
   - 风格：语气、人称、引用
   - 约束：敏感内容、合规

3. **信心门槛（~95%）**
   达到后用结构化摘要确认：

   > **目标：** …
   > - **受众：** …
   > - **范围/要点：** …
   > - **语气与风格：** …
   > - **目标路径：** `docs/articles/<slug>.md`
   >
   > **假设**（如有错误请纠正）：
   > - …

   然后问："如果以上理解正确，我就开始写了。"

4. **撰写** — 用 GitHub 风格 Markdown，中文为主。写完后调用 commit_article 提交。

5. **讨论** — 文章存在后，用 IM 风格回答问题。不要主动改文件，除非用户明确要求修改。

6. **修订** — 用户要求改时，先用 get_article 读取当前版本，修改后再 commit_article 更新，简要说明改了什么。

## 默认（未指定时使用，标注为假设）
- 路径 `docs/articles/<kebab-case>.md`，直接提交到 main 分支
- 800–1500 字，中性专业语气

## 反模式
- 不要一次问多个问题
- 不要未经确认就猜测文件名
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "commit_article",
            "description": "将 Markdown 文章写入或更新到 GitHub 仓库。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "仓库内路径，如 docs/articles/my-topic.md",
                    },
                    "content": {
                        "type": "string",
                        "description": "文章完整 Markdown 内容",
                    },
                    "commit_message": {
                        "type": "string",
                        "description": "Git 提交信息",
                    },
                },
                "required": ["path", "content", "commit_message"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_article",
            "description": "读取仓库中已有文章内容，用于修订前获取当前版本。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "仓库内路径",
                    },
                },
                "required": ["path"],
            },
        },
    },
]


def get_history(chat_id: int) -> list[dict]:
    if chat_id not in sessions:
        sessions[chat_id] = []
    return sessions[chat_id]


def trim_history(history: list[dict]) -> list[dict]:
    if len(history) > MAX_HISTORY:
        del history[: len(history) - MAX_HISTORY]
    return history


def _execute_tool(name: str, arguments: str) -> str:
    args = json.loads(arguments)

    if name == "commit_article":
        result = commit_article(
            repo_name=GITHUB_REPO,
            path=args["path"],
            content=args["content"],
            commit_message=args["commit_message"],
            token=GITHUB_TOKEN,
        )
        return json.dumps(result, ensure_ascii=False)

    if name == "get_article":
        return get_article_content(
            repo_name=GITHUB_REPO,
            path=args["path"],
            token=GITHUB_TOKEN,
        )

    return json.dumps({"error": f"unknown tool: {name}"})


def call_llm(history: list[dict]) -> str:
    """Send history to LLM via OpenRouter, handle tool-use loops, return final text."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=4096,
        messages=messages,
        tools=TOOLS,
    )

    choice = response.choices[0]

    while choice.finish_reason == "tool_calls":
        assistant_msg = choice.message.model_dump()
        history.append(assistant_msg)

        for tool_call in choice.message.tool_calls:
            try:
                output = _execute_tool(tool_call.function.name, tool_call.function.arguments)
            except Exception as exc:
                output = f"Error: {exc}"

            history.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": output,
                }
            )

        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
        response = client.chat.completions.create(
            model=MODEL,
            max_tokens=4096,
            messages=messages,
            tools=TOOLS,
        )
        choice = response.choices[0]

    text = choice.message.content or ""
    history.append({"role": "assistant", "content": text})
    return text


async def _send(message, text: str) -> None:
    """Send a potentially long reply, splitting on paragraph boundaries."""
    MAX_LEN = 4000
    if not text:
        return

    if len(text) <= MAX_LEN:
        await message.reply_text(text)
        return

    chunks: list[str] = []
    current = ""
    for para in text.split("\n\n"):
        if current and len(current) + len(para) + 2 > MAX_LEN:
            chunks.append(current)
            current = para
        else:
            current = f"{current}\n\n{para}" if current else para
    if current:
        chunks.append(current)

    for chunk in chunks:
        await message.reply_text(chunk)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)

    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        await update.message.reply_text("你没有使用此机器人的权限。")
        return

    history = get_history(chat_id)
    history.append({"role": "user", "content": update.message.text})
    trim_history(history)

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        reply = call_llm(history)
    except Exception as exc:
        logger.exception("LLM API error")
        reply = f"出错了，请稍后重试。\n({exc})"

    await _send(update.message, reply)


async def cmd_start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "你好！我是文章助手。\n\n"
        "给我一个主题，我会通过提问了解你的需求，"
        "然后帮你生成一篇文章并提交到 GitHub。\n\n"
        "发送 /new 开始新会话。"
    )


async def cmd_new(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    sessions[update.effective_chat.id] = []
    await update.message.reply_text("已开始新会话。请给我一个主题。")


def main() -> None:
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("new", cmd_new))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot is running …")
    app.run_polling()


if __name__ == "__main__":
    main()
