# Validation Results Diagrams

## Three-system smoke check

`make smoke-embeddings` evaluates all three systems on the same 20 aligned
Sursilvan → Vallader queries and 20 candidates from the Mediomatix validation
split. The sample uses seed 13 and a 128-token limit for the embedding models.

```mermaid
xychart-beta
    title "Recall@1 on 20 Sursilvan to Vallader queries"
    x-axis ["TF-IDF", "MiniLM", "XLM-R"]
    y-axis "Recall@1" 0 --> 1
    bar [0.95, 0.85, 0.65]
```

| System | Correct at rank 1 | Recall@1 | MRR |
| --- | ---: | ---: | ---: |
| Character TF-IDF | 19 of 20 | 0.950 | 0.975 |
| Multilingual MiniLM | 17 of 20 | 0.850 | 0.892 |
| Pretrained XLM-R | 13 of 20 | 0.650 | 0.749 |

With the dependencies and validation data set up, rerun the smoke check and
summarize its CSV by model and overlap bucket.

```bash
make smoke-embeddings
python3 scripts/summarize_report.py reports/smoke_embeddings/retrieval_validation.csv
```

## TF-IDF validation across 20 idiom directions

This run evaluates character TF-IDF on 500 aligned rows per direction, for
10,000 retrieval queries. The figures in this section use that sample.

```bash
python3 scripts/run_retrieval.py --split validation --methods tfidf --max-rows 500
```

### Classification blob view

![Lexical-overlap classification blobs](assets/classification_blobs.svg)

This view shows the bucket assignment visually: rows are first separated by
their pair-specific lexical-overlap quantiles, then each bucket is evaluated.

### Result blob view

![TF-IDF validation results by overlap bucket](assets/result_blobs.svg)

TF-IDF Recall@1 drops from 0.978 in the high-overlap bucket to 0.540 in the
low-overlap bucket.

### Process, classification, and results

```mermaid
flowchart LR
    P["Process<br/>20 idiom directions<br/>500 rows each<br/>10,000 queries"] --> C["Classify<br/>low: 3,300 rows<br/>mid: 3,398 rows<br/>high: 3,302 rows"]
    C --> R["Results<br/>TF-IDF Recall@1<br/>low: 0.540<br/>mid: 0.923<br/>high: 0.978<br/>overall: 0.815"]
```

### Recall@1 by overlap bucket

```mermaid
xychart-beta
    title "TF-IDF Recall@1 by lexical-overlap bucket"
    x-axis ["Low", "Mid", "High", "All"]
    y-axis "Recall@1" 0 --> 1
    bar [0.540, 0.923, 0.978, 0.815]
```

### MRR by overlap bucket

```mermaid
xychart-beta
    title "TF-IDF MRR by lexical-overlap bucket"
    x-axis ["Low", "Mid", "High", "All"]
    y-axis "MRR" 0 --> 1
    bar [0.628, 0.951, 0.986, 0.856]
```

### Mean rank by overlap bucket

```mermaid
xychart-beta
    title "Gold target mean rank by lexical-overlap bucket"
    x-axis ["Low", "Mid", "High", "All"]
    y-axis "Mean rank" 0 --> 21
    bar [20.47, 1.22, 1.05, 7.52]
```

### Row distribution

```mermaid
pie showData
    title Validation rows by overlap bucket
    "low" : 3300
    "mid" : 3398
    "high" : 3302
```

### Easiest and hardest directions

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

### Low-overlap stress cases

```mermaid
flowchart TD
    A["Lowest Recall@1 in low-overlap rows"] --> B["rm-surmiran -> rm-puter<br/>0.339"]
    A --> C["rm-surmiran -> rm-vallader<br/>0.358"]
    A --> D["rm-sursilv -> rm-surmiran<br/>0.400"]
    A --> E["rm-puter -> rm-surmiran<br/>0.412"]
```

### Summary table

| Bucket | Rows | Recall@1 | MRR | Mean rank |
| --- | ---: | ---: | ---: | ---: |
| all | 10,000 | 0.815 | 0.856 | 7.52 |
| low | 3,300 | 0.540 | 0.628 | 20.47 |
| mid | 3,398 | 0.923 | 0.951 | 1.22 |
| high | 3,302 | 0.978 | 0.986 | 1.05 |
