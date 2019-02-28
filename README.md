* SQLite database-file: `https://figshare.com/articles/Patent_Database/7264733`
* Patent scoring by expert and corpus subsample: `https://figshare.com/articles/human_eval_tar_gz/7257215`
* Entire corpus: `https://figshare.com/articles/corpus_tar_gz/7257194`

* 原repo地址: `https://github.com/helmersl/patent_similarity_search`

* 原论文: `Automating the search for a patent’s prior art with a full text similarity search.pdf`

* 数据库访问示例: `process.py`

论文结果:
|Feature | | | AUC | | | AP
|-|-|-|-|-|-|-|-
| |subsample| |full|subsample| |full
| |relevant|cited|cited|relevant|cited|cited
|Bag-of-words|0.8118|0.8063|__0.9560__|0.5274|0.7095|__0.4705__
|LSA|0.7798|0.7075|0.9361|0.4787|0.5921|0.3257
|KPCA|0.7441|0.6740|0.9207|0.4721|0.5832|0.2996
|BOW+word2vec|__0.8408__|__0.8544__|0.9410|__0.5443__|__0.7354__|0.4019
|doc2vec|0.7658|0.8138|0.9314|0.4749|0.6829|0.3121