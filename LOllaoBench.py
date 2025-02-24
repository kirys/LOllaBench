#!/bin/env python3
from typing import List
import ollama as ollamaLib
import argparse
from datetime import datetime

ollama=None


from datetime import datetime


def run_benchmark(
 	model_name: str, prompt: str, verbose: bool
	):
	response = None
	response = ollama.chat(
		model=model_name,
		messages=[
			{
				"role": "user",
				"content": prompt,
			},
		]
	)
	if not response:
		print("System Error: No response received from ollama")
		return None
	if verbose:
		print(response)
	return response

def get_benchmark_models(skip_models: List[str] = []) -> List[str]:
	models = ollama.list().get("models", [])
	model_names = [model["model"] for model in models]
	if len(skip_models) > 0:
		model_names = [
			model for model in model_names if model not in skip_models
		]
	print(f"Evaluating models: {model_names}\n")
	return model_names

def nanosec_to_sec(nanosec):
	return nanosec / 1000000000

def calc_benchmarks(responses):
	prompt_time=0
	prompt_tokens=0
	response_time=0
	response_tokens=0
	for response in responses:
		prompt_time+=response['prompt_eval_duration']
		prompt_tokens+=response['prompt_eval_count']
		response_time+=response['eval_duration']
		response_tokens+=response['eval_count']
	return {
		'prompt_time':nanosec_to_sec(prompt_time),
		'prompt_tokens':prompt_tokens,
		'response_time':nanosec_to_sec(response_time),
		'response_tokens':response_tokens
		}

def longest_string_length(strings: List[str]) -> int:
	if not strings:
		return 0
	return max(len(s) for s in strings)

def main(args):
	print(args)
	server=args.server
	print (server)
	global ollama
	ollama = ollamaLib.Client(host=server)
	models=get_benchmark_models()
#	models= ['mistral-nemo:latest']
	ml=longest_string_length(models)+4

	print (models)
	prompts=[
			"Why is the sky blue?",
			"Write a report on the financials of Apple Inc.",
			"Write a modern version of the ciderella story.",
		]
	print (prompts)
	benchmarks = {}
	for model in models:
		responses= []
		for prompt in prompts:
			print(f"\n\nBenchmarking: {model}\nPrompt: {prompt}")
			response = run_benchmark(model, prompt, verbose=False)
			responses.append(response)
			#print(response)
			#print(f"Response: {response.message.content}")
		benchmarks[model]=calc_benchmarks(responses)
	print(benchmarks)
	print(ml)
	print(f'{"Model":<{ml}} {"Eval. Toks":>14} {"Resp. toks":>14} {"Total toks":>14}')
	for model,bench in benchmarks.items():
		prompttoks= bench['prompt_tokens']/bench['prompt_time']
		responsettoks= bench['response_tokens']/bench['response_time']
		totaltoks= (bench['prompt_tokens']+bench['response_tokens'])/(bench['response_time']+bench['prompt_time'])
		print(f'{model:<{ml}} {prompttoks:>14.2f} {responsettoks:>14.2f} {totaltoks:>14.2f}')



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('server', help="ollama server:port eg localhost:11434" )
	args = parser.parse_args()
	main(args)
