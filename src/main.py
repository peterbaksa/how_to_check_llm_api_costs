import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from src.common.file_handler import get_cwd


def call_openai_model(user_query: str, model: str, model_api_key: str):

    print("Waiting for the AI response...")
    llm = ChatOpenAI(
        model=model,
        api_key=model_api_key,
        temperature=0
    )

    ai_msg = llm.invoke([user_query])

    return ai_msg


# https://openai.com/api/pricing/
model_prices = {
    "gpt-4.1": {"input": 2.0/1_000_000, "output": 8.0/1_000_000, 'cached': 0.5/1_000_000},
    "gpt-4.1-mini": {"input": 0.4/1_000_000, "output": 1.6/1_000_000, 'cached': 0.1/1_000_000},
    "gpt-4.1-nano": {"input": 0.1/1_000_000, "output": 0.4/1_000_000, 'cached': 0.025/1_000_000}
    }

if __name__ == "__main__":
    CWD = get_cwd("how_to_check_llm_api_costs")
    if load_dotenv(os.path.join(CWD, ".env")):
        openai_api_key = os.getenv("OPENAI_API_KEY")
        model_name = "gpt-4.1-mini"

        if openai_api_key:
            my_question = "Describe me how to check LLM API costs"
            ai_message = call_openai_model(my_question, model_name, openai_api_key)

            # print all keys/parameters of the AI message
            # print(*dict(ai_message).keys(), sep="\n")
            ''' ----- Output -----
                content
                additional_kwargs
                response_metadata
                type
                name
                id
                example
                tool_calls
                invalid_tool_calls
                usage_metadata
            '''

            # to print the content (text response) of the AI message
            print(ai_message.content, "\n\n")

            # Let's now calculate the cost of the response
            count_of_input_tokens = ai_message.usage_metadata.get("input_tokens", 0)
            count_of_output_tokens = ai_message.usage_metadata.get("output_tokens", 0)

            model_token_prices = model_prices.get(model_name, None)
            if model_token_prices:
                input_cost = count_of_input_tokens * model_token_prices["input"]
                output_cost = count_of_output_tokens * model_token_prices["output"]
                total_cost = input_cost + output_cost

                print(f"Input tokens: {count_of_input_tokens}, Cost: ${input_cost:.6f}")
                print(f"Output tokens: {count_of_output_tokens}, Cost: ${output_cost:.6f}")
                print(f"Total cost for this response: ${total_cost:.6f}")

                ''' ----- Example Output -----
                    Input tokens: 16, Cost: $0.000006
                    Output tokens: 450, Cost: $0.000720
                    Total cost for this response: $0.000726
                '''

            else:
                print(f"Error: Model '{model_name}' not found in pricing data.")

        else:
            "Error: OPENAI_API_KEY is not set in the environment."
    else:
        print("Error: .env file not found or could not be loaded.")

    # input()

''' ----- Example Output -----
AIMessage(
	content='To check the costs of using a Large Language Model (LLM) API, you generally need to follow these steps:
	\n\n1. **Visit the Provider’s Pricing Page**  \n   Most LLM API providers (like OpenAI, Google, Microsoft, 
	Anthropic, etc.) have a dedicated pricing page on their website. This page outlines the cost structure, including 
	rates per token, per request, or per usage tier.\n\n2. **Understand Pricing Units**  \n   - **Tokens:** Many LLM 
	APIs charge based on tokens processed (input + output). A token can be roughly a word or part of a word.  \n   
	- **Requests:** Some APIs charge per API call or per batch of calls.  \n   - **Compute Time:** Less common, but 
	some providers charge based on compute time or GPU hours.\n\n3. **Check Your Usage Dashboard**  \n   If you have 
	an account with the provider, log in to the developer console or dashboard. Most providers show:  \n   - Your 
	current usage (tokens used, requests made)  \n   - Estimated or actual costs incurred so far  \n   - Billing 
	history and invoices\n\n4. **Use Cost Estimators or Calculators**  \n   Some providers offer cost calculators 
	where you can input expected usage (e.g., number of tokens per request, number of requests per month) to estimate 
	monthly costs.\n\n5. **Review Billing and Subscription Plans**  \n   Check if there are subscription tiers, free 
	quotas, or volume discounts that affect your costs.\n\n6. **Monitor Usage Programmatically**  \n   Some APIs 
	provide usage endpoints or metrics you can query programmatically to track your consumption and estimate costs 
	in real-time.\n\n---\n\n### Example: Checking OpenAI API Costs\n\n- Go to [OpenAI Pricing]
	(https://openai.com/pricing) to see rates per model (e.g., GPT-4, GPT-3.5).  \n- Log in to your OpenAI account 
	and visit the usage dashboard at [OpenAI Platform Usage](https://platform.openai.com/account/usage) to see your 
	token usage and estimated costs.  \n- Use the pricing info to calculate costs based on your usage.\n\n---\n\nIf 
	you tell me which LLM API you are using, I can provide more specific instructions!', 
	
	additional_kwargs={'refusal': None}, 
	
	response_metadata={
		'token_usage': {
			'completion_tokens': 454, 
			'prompt_tokens': 16, 
			'total_tokens': 470, 
			completion_tokens_details': {
				'accepted_prediction_tokens': 0, 
				'audio_tokens': 0, 
				'reasoning_tokens': 0, 
				'rejected_prediction_tokens': 0
			}, 
			'prompt_tokens_details': {
				'audio_tokens': 0, 
				'cached_tokens': 0
				}
			}, 
		
		'model_name': 'gpt-4.1-mini-2025-04-14', 
		'system_fingerprint': None, 
		'id': 'chatcmpl-Bw2JaF9gIZLQpK2q5fU8BkU5Os6h6', 
		'service_tier': 'default', 
		'finish_reason': 'stop', 
		'logprobs': None
		}, 
	
	id='run--cef5d191-72bb-4e38-90db-59ba4a89141f-0', 

	usage_metadata={
		'input_tokens': 16, 
		'output_tokens': 454, 
		'total_tokens': 470, 
		'input_token_details': {'audio': 0, 'cache_read': 0}, 
		'output_token_details': {'audio': 0, 'reasoning': 0}})

'''