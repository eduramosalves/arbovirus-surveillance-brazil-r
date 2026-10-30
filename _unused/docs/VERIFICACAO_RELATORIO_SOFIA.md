# Verificação das recomendações de `RELATORIO_REVISAO_SOFIA.R`

Data: 2026-10-14. Escopo: os 9 itens que você marcou como **ACHO BOM VERIFICAR** (R1, R8, R10, M2, M4, M6, M7) ou **OLHAR EM PYTHON** (R2, R5). Os 11 itens marcados como DESNECESSARIO não foram verificados.

**Nenhum arquivo de código ou de resultado do projeto foi alterado.** `check_db.R` deu o mesmo resultado antes e depois (5 CSVs OK; os 3 `.xlsx` diferem só pelo timestamp, como esperado) e `git status` ficou limpo. O único arquivo novo é este.

Fonte do Python original: `arbovirus-brazil-portable.rar` (OneDrive, lido sem extrair), com `mapclassify 2.10.0`, `numpy 2.4.5`, `scipy 1.17.1`, `scikit-learn 1.9.1`, `pandas 3.0.3`. Dados brutos INMET: cópia do OneDrive, com os 11 zips conferidos contra `raw/MANIFEST.csv` (sha256 idêntico).

## Resumo

| Item | Veredito | Muda algum resultado publicado? | Ação sugerida |
|---|---|---|---|
| **R1** `Classfication` | **Refutado.** O R está certo. | Não | **Não corrigir.** "Corrigir" faria `find_table()` dar `stop()`. |
| **R2** `jenks` vs `fisher` | **Refutado como bug.** | Não | **Não trocar** para `fisher`. Mudaria os números da legenda. |
| **R5** `sd()` / ddof | **Refutado.** | Não | Nenhuma. |
| **R8** `solve()` sem `tryCatch` | Risco latente confirmado, **não ocorre** nos dados. | Não | Opcional: fallback `ginv` (no-op hoje). |
| **R10** espaço em campo INMET | Premissa correta, **zero ocorrências** nos dados. | Não | Nenhuma obrigatória. |
| **M2** n do t-teste da co-circulação | Confirmado. Impacto mínimo. | Não | Decisão sua (ver abaixo). |
| **M4** `t_since_pandemic` | Confirmado como questão de **interpretação**. Port fiel ao Python. | Não | Renomear/documentar a coluna. |
| **M6** ordem de arredondamento dos lags | **OK**, idêntico ao Python. | Não | Nenhuma. |
| **M7** `py_float_str` | Confirmado. **Sem impacto** nos dados. | Não | Nenhuma. |

---

## R1: "Classfication" (CHIKV) vs "Classification" (ZIKV)

**Veredito: refutado. O erro de grafia está no arquivo do Prism, e o R o reproduz corretamente.**

- Títulos reais das tabelas (lidos com `read_tables()` de `graphpad_pipeline.R`): Chikungunya = `Classfication 2017-2025`; Zika = `Classification 2016-2025`. Também em `db/graphpad_data/…chikungunya….pzfx:1038` e `reference/graphpad_data/…:1038`.
- Os 20 pares (vírus, prefixo) usados em `build_source_data.R` casam **exatamente 1** tabela cada via `startsWith`.
- Aplicando a "correção" sugerida (`"Classification"` para Chikungunya): **0 tabelas casam**, então `find_table()` daria `stop("table not found")`.
- O Python original (`build_source_data.py`) usa `"Classfication"` e o `graphpad_to_python_pipeline.py` anota `# Prism file typo`. O R já trata os dois casos em `graphpad_pipeline.R:88,197,348`.
- A aba `Fig8A1_Chik_Classfic` existe em `source_data/Figure8.xlsx`.

## R2: `natural_breaks()` usa `"jenks"`; deveria ser `"fisher"`?

**Veredito: refutado como bug. Não trocar.**

O Python usa `mapclassify.NaturalBreaks`, que é **k-means 1-D com 10 inicializações** (`classifiers.py`, `natural_breaks(values, k, init=10)`), e não `FisherJenks`. Testei com os dados reais (Figura 6: média por UF, n=27 por vírus; Figura S1: incidência por UF-ano, n≈296):

- **R `jenks` = Python `FisherJenks`** (limites iguais) nos 6 conjuntos. Ambos são o ótimo exato (mesma soma de quadrados intra-classe).
- **R `jenks` e R `fisher` dão as mesmas classes** nos 6 conjuntos. Mas os **limites diferem**: o `fisher` devolve pontos médios entre classes, enquanto o `jenks` devolve o maior valor de cada classe, que é a convenção do `bins` do mapclassify. Exemplo (Chikungunya, Fig. 6):
  - `jenks`: 67,25 | 135,70 | 196,58 | 324,94 | 498,37
  - `fisher`: 81,08 | 142,49 | 218,93 | 411,65 | 498,37

  Trocar para `fisher` manteria as classes, mas **alteraria os números da legenda "Class bounds"** e da aba `Fig6_class_bounds`.
- O `NaturalBreaks` do Python é **estocástico**. Em 300 execuções, a fração que coincide com o ótimo exato foi de ≈87% (Chik), 100% (Dengue) e ≈89% (Zika) na Fig. 6, e ≈7%, ≈58% e ≈32% na Fig. S1 (varia alguns pontos entre rodadas). Quando diverge, a soma de quadrados sobe (Chik Fig. 6: 12.119,11 → 12.425,20; Zika: 1.163,99 → 1.166,79) e 2 a 7 UFs de 27 mudam de classe na Fig. 6.

**Conclusão:** o R produz o ótimo determinístico. A figura publicada na era Python veio de uma única execução aleatória do k-means. Se algum mapa da era Python diferir do R na classe de uma UF, a causa é essa aleatoriedade, não um erro do R. (As planilhas da era Python não guardam as classes, então não dá para comparar a execução publicada UF a UF.)

## R5: `sd()` usa ddof = 1; e o Python?

**Veredito: refutado.** `bootstrap_ci.py:62,77` usa `cases.std(ddof=1)` e `inc.std(ddof=1)`, igual ao `sd()` do R.

Comparação empírica entre os arquivos do Python (no `.rar`) e os do R no repo:

| Arquivo | Mean, Normal_CI_Lower/Upper, n | Bootstrap_CI (Monte Carlo) |
|---|---|---|
| `bootstrap_ci_95_cases.csv` | diferença máx. **0** | até 1,2% (RNG diferente, esperado) |
| `bootstrap_ci_95_incidence.csv` | diferença máx. **7,1e-15** | até 0,8% (idem) |

(O `arbovirus_project_files.zip` de Downloads é de outra safra, com n diferente, e não serve de referência.)

## R8: `solve()` sem `tryCatch` em `adv_dlnm.R:98`

**Veredito: risco latente confirmado, mas não ocorre.** Replicando `adv_dlnm.R:74-98` para os 3 vírus:

| Vírus | n | colunas de X | posto (qr) | rcond(X'WX) | `solve()` |
|---|---|---|---|---|---|
| Dengue | 3.309 | 48 | 48 (cheio) | 1,9e-05 | ok |
| Chikungunya | 3.295 | 48 | 48 (cheio) | 2,2e-05 | ok |
| Zika | 3.268 | 48 | 48 (cheio) | 2,9e-05 | ok |

- O limite em que o `solve()` aborta é rcond < 2,2e-16, então há ~11 ordens de grandeza de folga.
- `solve()` vs `MASS::ginv()`: diferença relativa máxima na diagonal de V de **1,0e-13**, **9,7e-14** e **5,8e-13**. Um fallback para `ginv` seria **no-op** com esses dados.
- Teste de robustez: com uma coluna duplicada em X, o `solve()` falha ("system is exactly singular") e o `ginv()` funciona.
- **Nuance:** o `tryCatch` da linha 92 cobre só `fit_negbin()`. Uma matriz singular na linha 98 abortaria o `run()` inteiro (os 3 vírus e a figura), em vez de pular um vírus.
- Os outros `solve(` do projeto (`glm_common.R:133,187,209`) estão dentro de `fit_family()`, protegido pelo `tryCatch` de `run_models()` (`glm_common.R:276`): uma falha vira "fit failed" e o modelo é pulado.

Patch proposto, **não aplicado**:
```r
XtWX <- crossprod(X, X * oim_factor(sub$Cases, f$mu, nb$alpha))
V <- tryCatch(solve(XtWX), error = function(e) MASS::ginv(XtWX))
```

## R10: `strip.white = FALSE` e tokens com espaço no INMET

**Veredito: a premissa é correta em teoria, mas não há ocorrência nos dados.**

- O pandas 3.0.3 de fato aceita campo numérico com espaço (`" 21,5"` → 21,5; testado). O parser do R (`parse_decimal_comma`) daria NA.
- Varredura de **todos** os CSVs de estação, 2016–2026 (11 zips, 7.023 CSVs, incluindo os snapshots antigos duplicados), lendo as colunas 1/3/8 com os mesmos parâmetros de `build_climate.R:93-95` e a regex copiada literalmente:
  - **114.760.176** tokens de chuva/temperatura: **0** com espaço no início ou fim, **0** não vazios que viram NA.
  - Datas rejeitadas por `parse_ym`: **0**.
- **Prova ponta a ponta:** rodei `etl/build_climate.R` do zero sobre os zips brutos, numa cópia isolada (107 s). O `normalized_fact_climate.csv` regenerado tem sha256 `8295ef79…cc9e6e`, **idêntico** ao de `reference/expected_hashes.csv`.
- Sibling: `etl/build_cases_clinical.R:113` (`strip.white = FALSE` no SINAN). O Python original também não aplica `strip` em `SG_UF_NOT` e `DT_NOTIFIC`, e os hashes de `normalized_fact_cases.csv` e `clinical_demographic_long.csv` batem. Não fiz varredura de tokens no SINAN, por redundância com o hash.

## M2: p-valor "naive" da co-circulação

**Veredito: confirmado, impacto mínimo.** O Python usa o mesmo `n_eff = isfinite(a).sum()` (`adv_cocirculation.py`), então o port é fiel. O n correto seria o número de pares realmente correlacionados no melhor lag (n menos |lag| menos NAs de b).

Recalculei os 99 pares (nacional + 5 regiões + 27 estados, × 3 pares de vírus). O p "naive" reproduz o CSV do repo (diferença 0) e o do Python (2,8e-16).

- Diferença de n: mínimo 0, mediana 1, máximo 19. Em 22 linhas há NAs de b além do deslocamento do lag.
- Razão p_corrigido/p_naive: mediana 1,028 (o máximo, 7.084, ocorre em p minúsculos e não muda a conclusão).
- Significância nominal (p<0,05): **81 → 81** significativos, **17 → 17** não, **1** linha muda: São Paulo, Chikungunya–Zika, lag 1 (p = 0,0493 → 0,0503).
- FDR (q<0,05) nos 81 casos estaduais: **0 mudanças**.

As limitações maiores (escolha do melhor entre 13 lags, autocorrelação) seguem como já documentadas em `R_PORT_NOTES.md`. Corrigir o n mudaria levemente todos os p publicados; sugiro manter e, se quiser, citar a limitação no texto.

## M4: `t_since_pandemic` só é diferente de zero dentro da janela

**Veredito: confirmado como questão de interpretação. O port é fiel ao Python** (`np.where(pandemic>0, months_in, 0)`).

- Nível e rampa estão **ambos confinados** à janela mar/2020–dez/2021 (22 meses). É um design de **pulso** coerente, mas a coluna `slope_change_per_month` **não** é uma mudança de tendência pós-intervenção permanente. Ela vale a deriva dentro da janela e zera em jan/2022.
- Reproduzi o CSV do repo (diferença 0) e o do Python (4,6e-13).
- **Consequência de leitura:** `pandemic_pct_change` (−26%, −54%, −37% nas legendas) é o efeito **no início da janela** (mar/2020), e não um efeito médio. No nacional, o efeito evolui assim dentro da janela:

  | Vírus | início | meio | fim |
  |---|---|---|---|
  | Dengue | −25,6% | −30,6% | −35,3% |
  | Chikungunya | −53,6% | −36,3% | −12,6% |
  | Zika | −37,4% | −25,6% | −11,5% |

  Em 97 séries, a diferença entre início e meio da janela tem mediana de 17,7 pontos percentuais, e o sinal muda em 14.
- **Sensibilidade à especificação** (não é uma correção, só uma medida de fragilidade): mantendo o dummy de janela e deixando a rampa crescer após a janela, 51 das 97 séries mudam de conclusão (p<0,05). Nacional: Dengue −25,6% → −46,6% (p 0,30 → 0,022); Chikungunya −53,6% → −26,4% (p 1e-05 → 0,053); Zika −37,4% → +5,2% (p 0,013 → 0,78). Isso mostra que o efeito estimado depende da especificação.

Sugestão: sem alterar números, descrever a coluna como "inclinação dentro da janela (22 meses)" e o `pandemic_pct_change` como "efeito no início da janela".

## M6: lags calculados sobre valores já arredondados

**Veredito: OK, idêntico ao Python.** `build_climate.py` ordena por `Location_ID, Year, Month`, arredonda `Temp_Avg` e `Rain_mm` a 2 casas e só então faz `groupby.shift(lag).round(2)`. `build_climate.R:140-144` faz a mesma sequência. Reforçado pela reprodução byte a byte do `normalized_fact_climate.csv` (ver R10).

## M7: `py_float_str()` aproxima o `repr()` do Python

**Veredito: confirmado, sem impacto nos dados.** Teste com 200.025 doubles (magnitudes 1e-20…1e20, faixas de fronteira, valores x,xx5) comparando com `repr(float)` do Python 3.14:

- **Magnitude normal [1e-4, 1e15):** 10 divergências em 133.180 (0,0075%). Em 7 o R imprime um dígito a mais mas relido dá o mesmo double. Em 3 a string do R, relida pelo Python, dá um double 1 ULP diferente (o `as.numeric` do R não é arredondado corretamente em strings longas, e o teste de ida e volta interno aceita esse caso).
- **Fronteira de formato:** a escada 15/16/17 g difere do Python em [1e15, 1e17): o R usa notação científica a partir de 1e15 para valores de ≤15 dígitos e o Python a partir de 1e16. Também em denormais (ex.: `5e-324`).
- **Impacto real:** nas 146.762 células float dos 33 CSVs do projeto, **5** (0,0034%) têm texto diferente do `repr` Python do mesmo valor, todas em `outputs/` (fora do `expected_hashes.csv`) e todas com **o mesmo double**, só com um dígito a mais (ex.: `313.64203389830533` em vez de `313.6420338983053`) e um denormal (`1.77863632502849e-322` em vez de `1.8e-322`). Nenhuma célula cai nas faixas de fronteira: as 2 células em [1e15, 1e16) têm 17 dígitos e batem com o Python. Os CSVs cobertos por hash são byte-idênticos.

---

## Varredura de ocorrências irmãs

| Padrão | Onde | Situação |
|---|---|---|
| `Classfication` | `build_source_data.R:236`, `graphpad_pipeline.R:88,197,348`, `figure_exclusions.csv`, `figure_caption_values.csv` | Propaga o título do Prism. Idêntico ao Python. |
| `strip.white = FALSE` | `build_climate.R:94`, `build_cases_clinical.R:113` | Fiel ao Python. Zero tokens com espaço no INMET. |
| `solve(` | `glm_common.R:133,187,209`; `adv_dlnm.R:98` | Os três primeiros estão protegidos por `run_models`. Só o de `adv_dlnm.R` não. |
| p-valor com n fixo | `adv_cocirculation.R:86-88` | Único ponto, tratado em M2. |

## Itens não verificados (por sua decisão)

R3, R4, R6, R7, R9, M1, M3, M5, M8, M9, M10 (marcados "DESNECESSARIO").

## Reprodução

Os scripts de verificação ficaram só no scratchpad temporário da sessão (R e Python, sem tocar no repo). Se quiser mantê-los, posso salvá-los em `tools/verificacao/`.
