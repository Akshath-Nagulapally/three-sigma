import os


code_gen_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_message_with_imports,
        ),
        ("placeholder", "{messages}"),
    ]
)


reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a coding assistant with expertise in debugging. Given code and an error message from a compiler, you will reflect on it and suggest the changes required to make the code correct""",
        ),
        ("placeholder", "{messages}"),
    ]
)


class code(BaseModel):
    """Schema for code solutions."""

    prefix: str = Field(description="detailed technical description of the problem and approach")
    imports: str = Field(description="Code block import statements")
    code: str = Field(description="Code block not including import statements, must be a class named MyStrategy")

class reflection(BaseModel):
    """Schema for reflection on code errors."""

    analysis: str = Field(description="Analysis and reflection of the problem and approach")
    action: str = Field(description="instruction on what to do to fix the error")


model = os.getenv("MODEL_CHOICE")


if model == "openai":
  expt_llm = "gpt-4o-mini"
  OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
  llm = ChatOpenAI(temperature=0, api_key = OPENAI_API_KEY, model=expt_llm)
else:
  expt_llm = "llama-3.3-70b-versatile"
  GROQ_API_KEY = os.getenv("GROQ_API_KEY")
  llm = ChatGroq(model=expt_llm, api_key = GROQ_API_KEY, max_tokens=8192)

code_gen_chain_oai = code_gen_prompt | llm.with_structured_output(code)
reflection_chain = reflection_prompt | llm.with_structured_output(reflection)