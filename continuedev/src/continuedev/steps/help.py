from textwrap import dedent
from ..core.main import ChatMessage, Step
from ..core.sdk import ContinueSDK
from ..libs.util.telemetry import capture_event

help = dedent("""\
        Continue is an open-source coding autopilot. It is a VS Code extension that brings the power of ChatGPT to your IDE.
              
        It gathers context for you and stores your interactions automatically, so that you can avoid copy/paste now and benefit from a customized Large Language Model (LLM) later.

        Continue can be used to...
        1. Edit chunks of code with specific instructions (e.g. "/edit migrate this digital ocean terraform file into one that works for GCP")
        2. Get answers to questions without switching windows (e.g. "how do I find running process on port 8000?")
        3. Generate files from scratch (e.g. "/edit Create a Python CLI tool that uses the posthog api to get events from DAUs")

        You tell Continue to edit a specific section of code by highlighting it. If you highlight multiple code sections, then it will only edit the one with the purple glow around it. You can switch which one has the purple glow by clicking the paint brush.

        If you don't highlight any code, then Continue will insert at the location of your cursor.

        Continue passes all of the sections of code you highlight, the code above and below the to-be edited highlighted code section, and all previous steps above input box as context to the LLM.

        You can use cmd+m (Mac) / ctrl+m (Windows) to open Continue. You can use cmd+shift+e / ctrl+shift+e to open file Explorer. You can add your own OpenAI API key to VS Code Settings with `cmd+,`

        If Continue is stuck loading, try using `cmd+shift+p` to open the command palette, search "Reload Window", and then select it. This will reload VS Code and Continue and often fixes issues.

        If you have feedback, please use /feedback to let us know how you would like to use Continue. We are excited to hear from you!""")


class HelpStep(Step):

    name: str = "Help"
    user_input: str
    manage_own_chat_context: bool = True
    description: str = ""

    async def run(self, sdk: ContinueSDK):

        question = self.user_input

        prompt = dedent(f"""Please us the information below to provide a succinct answer to the following quesiton: {question}
                    
                    Information:

                    {help}""")

        self.chat_context.append(ChatMessage(
            role="user",
            content=prompt,
            summary="Help"
        ))
        messages = await sdk.get_chat_context()
        generator = sdk.models.gpt4.stream_chat(messages)
        async for chunk in generator:
            if "content" in chunk:
                self.description += chunk["content"]
                await sdk.update_ui()

        capture_event(sdk.ide.unique_id, "help", {
                      "question": question, "answer": self.description})
