
import os
os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["USE_TF"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from rouge_score import rouge_scorer
import json
from bert_score import score

with open("database.json", "r", encoding="utf-8") as f:
    data = json.load(f)

references = [item["input_text"] for item in data]
hypotheses = [item["summary"] for item in data]

scorer = rouge_scorer.RougeScorer(['rouge2'], use_stemmer=True)

scores = [scorer.score(ref, hyp)['rouge2'] for ref, hyp in zip(references, hypotheses)]

avg_precision = sum(s.precision for s in scores) / len(scores)
avg_recall = sum(s.recall for s in scores) / len(scores)
avg_fmeasure = sum(s.fmeasure for s in scores) / len(scores)

print("\n📌 ROUGE-2 Average Scores:")
print(f"Precision: {avg_precision:.4f}")
print(f"Recall:    {avg_recall:.4f}")
print(f"F1-score:  {avg_fmeasure:.4f}")

P, R, F1 = score(
    hypotheses,
    references,
    model_type="xlm-roberta-large",
    verbose=True
)


print("\n📌 BERTScore (mean):")
print(f"Precision: {P.mean().item():.4f}")
print(f"Recall:    {R.mean().item():.4f}")
print(f"F1-score:  {F1.mean().item():.4f}")
