import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function

def main():
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("no api key")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    prompt_print = args.user_prompt

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
                ),
            )



        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.function_calls:
            function_results = []

            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)

                if not function_call_result.parts:
                    raise RuntimeError("function_call_result has no parts")
                
                part = function_call_result.parts[0]
                if part.function_response is None:
                    raise RuntimeError("no function_response in part")

                if part.function_response.response is None:
                    raise RuntimeError("no response in function_response")
                
                function_results.append(part)

                if args.verbose:
                    print(f"-> {part.function_response.response}")

            messages.append(types.Content(role="user", parts=function_results))
        else:
            print(response.text)
            break

    if not response.usage_metadata:
        raise RuntimeError("no metadata")
        
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if args.verbose:
        print(f"User prompt: {prompt_print}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

if __name__ == "__main__":
    main()
