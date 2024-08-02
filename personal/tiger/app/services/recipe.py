from langchain_openai import ChatOpenAI


def generate_recipe(user_data, user_prompt):
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.7,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # The API key is loaded from the environment variable OPENAI_API_KEY
    )
    messages = [
        (
            "system",
            "You are a chef specializing in diabetic-friendly recipes. You give easy to follow recipes for home cooks given their profiles and food preferences.",
        ),
        (
            "user",
            f"Generate a diabetic-friendly recipe for a {user_data['age']}-year-old, {user_data['weight']} kg, {user_data['height']} cm person from {user_data['nationality']} who prefers {user_data['food_preferences']}. Summarize the user profile in your response.",
        ),
        (
            "assistant",
            "Alright! What kind of food do you want to have today?",
        ),
        (
            "user",
            user_prompt,
        ),
    ]
    try:
        response = llm.invoke(messages)
    except Exception as e:
        print(e)
        raise Exception("LLM invocation failed")

    return response.content
