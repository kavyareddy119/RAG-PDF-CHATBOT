from datasets import Dataset
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from ragas import evaluate

# Sample results — replace with your own
data = [
    {
        "question": "Who founded Apple?",
        "answer": "Steve Jobs, Steve Wozniak, and Ronald Wayne",
        "contexts": ["Apple was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in 1976."],
        "ground_truth": "Steve Jobs, Steve Wozniak, and Ronald Wayne"
    },
    {
        "question": "What product did Apple first release?",
        "answer": "The Apple I",
        "contexts": ["Apple I was the first product released by Apple in 1976."],
        "ground_truth": "Apple I"
    }
]

dataset = Dataset.from_list(data)
results = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision])
print("📊 RAG Evaluation Metrics:")
print(results)
