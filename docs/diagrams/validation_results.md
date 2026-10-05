# Actual Validation Results Diagrams

These diagrams summarize the current TF-IDF validation smoke run:

```bash
python3 scripts/run_retrieval.py --split validation --methods tfidf --max-rows 500
```

The run covers all 20 ordered source-target idiom pairs with 500 aligned rows
per pair, for 10,000 retrieval queries in total.

## PCR: Actual Run

```mermaid
flowchart LR
    P["Process<br/>20 idiom directions<br/>500 rows each<br/>10,000 queries"] --> C["Classify<br/>low: 3,300 rows<br/>mid: 3,398 rows<br/>high: 3,302 rows"]
    C --> R["Results<br/>TF-IDF Recall@1<br/>low: 0.540<br/>mid: 0.923<br/>high: 0.978<br/>overall: 0.815"]
```

## Recall@1 By Overlap Bucket

```mermaid
xychart-beta
    title "TF-IDF Recall@1 by lexical-overlap bucket"
    x-axis ["Low", "Mid", "High", "All"]
    y-axis "Recall@1" 0 --> 1
    bar [0.540, 0.923, 0.978, 0.815]
```

## MRR By Overlap Bucket

```mermaid
xychart-beta
    title "TF-IDF MRR by lexical-overlap bucket"
    x-axis ["Low", "Mid", "High", "All"]
    y-axis "MRR" 0 --> 1
    bar [0.628, 0.951, 0.986, 0.856]
```

## Mean Rank By Overlap Bucket

```mermaid
xychart-beta
    title "Gold target mean rank by lexical-overlap bucket"
    x-axis ["Low", "Mid", "High", "All"]
    y-axis "Mean rank" 0 --> 21
    bar [20.47, 1.22, 1.05, 7.52]
```

## Row Distribution

```mermaid
pie showData
    title Validation rows by overlap bucket
    "low" : 3300
    "mid" : 3398
    "high" : 3302
```

## Easiest And Hardest Directions

```mermaid
flowchart TD
    A["All-pair TF-IDF validation results"] --> B["Easiest directions"]
    A --> C["Hardest directions"]
    B --> B1["rm-puter -> rm-vallader<br/>Recall@1 0.974<br/>MRR 0.979"]
    B --> B2["rm-vallader -> rm-puter<br/>Recall@1 0.966<br/>MRR 0.975"]
    B --> B3["rm-sutsilv -> rm-sursilv<br/>Recall@1 0.908<br/>MRR 0.934"]
    C --> C1["rm-puter -> rm-sutsilv<br/>Recall@1 0.738<br/>MRR 0.799"]
    C --> C2["rm-surmiran -> rm-puter<br/>Recall@1 0.742<br/>MRR 0.800"]
    C --> C3["rm-surmiran -> rm-vallader<br/>Recall@1 0.744<br/>MRR 0.803"]
```

## Low-Overlap Stress Cases

```mermaid
flowchart TD
    A["Lowest Recall@1 in low-overlap rows"] --> B["rm-surmiran -> rm-puter<br/>0.339"]
    A --> C["rm-surmiran -> rm-vallader<br/>0.358"]
    A --> D["rm-sursilv -> rm-surmiran<br/>0.400"]
    A --> E["rm-puter -> rm-surmiran<br/>0.412"]
```

## Actual Summary Table

| Bucket | Rows | Recall@1 | MRR | Mean rank |
| --- | ---: | ---: | ---: | ---: |
| all | 10,000 | 0.815 | 0.856 | 7.52 |
| low | 3,300 | 0.540 | 0.628 | 20.47 |
| mid | 3,398 | 0.923 | 0.951 | 1.22 |
| high | 3,302 | 0.978 | 0.986 | 1.05 |

## Main Takeaway

TF-IDF is already very strong when idioms share spelling patterns. The low-overlap
bucket is the real stress test: performance drops sharply there, which supports
the project motivation for comparing lexical retrieval against semantic
zero-shot embeddings.
