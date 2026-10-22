# Computes every number quoted in the manuscript from the repository's own files.
# Output: numbers.csv  (key, value, src).  Raw values only; the builder formats them.
suppressPackageStartupMessages({library(readxl); library(data.table)})
ROOT <- "C:/Users/Usuario/arbovirus-surveillance-brazil-r-eduardo"
OUTF <- file.path(dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1]), winslash = "/")), "numbers.csv")
setwd(ROOT)

rows <- list()
add <- function(key, value, src) {
  v <- if (is.numeric(value)) format(value, digits = 15, scientific = FALSE, trim = TRUE) else as.character(value)
  rows[[length(rows) + 1]] <<- data.table(id = key, value = v, src = src)
}
sheet <- function(f, s) as.data.table(read_excel(f, sheet = s))
VC <- c(Dengue = "DENV", Chikungunya = "CHIKV", Zika = "ZIKV")
DIS <- c("DENV", "CHIKV", "ZIKV")
RC <- c(Norte = "N", Nordeste = "NE", Sudeste = "SE", Sul = "S", `Centro-Oeste` = "CO", Brazil = "BR")
strip <- function(x) chartr("\u00e1\u00e0\u00e2\u00e3\u00e9\u00ea\u00ed\u00f3\u00f4\u00f5\u00fa\u00e7", "aaaaeeiooouc", tolower(x))
UFNAME <- c(AC = "Acre", AL = "Alagoas", AP = "Amap\u00e1", AM = "Amazonas", BA = "Bahia", CE = "Cear\u00e1",
            DF = "the Federal District", ES = "Esp\u00edrito Santo", GO = "Goi\u00e1s", MA = "Maranh\u00e3o", MT = "Mato Grosso",
            MS = "Mato Grosso do Sul", MG = "Minas Gerais", PA = "Par\u00e1", PB = "Para\u00edba", PR = "Paran\u00e1",
            PE = "Pernambuco", PI = "Piau\u00ed", RJ = "Rio de Janeiro", RN = "Rio Grande do Norte", RS = "Rio Grande do Sul",
            RO = "Rond\u00f4nia", RR = "Roraima", SC = "Santa Catarina", SP = "S\u00e3o Paulo", SE = "Sergipe", TO = "Tocantins")
join_names <- function(ufs) {
  n <- unname(UFNAME[ufs]); k <- length(n)
  if (k == 0) return("none")
  if (k == 1) return(n)
  paste0(paste(n[-k], collapse = ", "), " and ", n[k])
}

# ---------------- location lookups ----------------
L <- fread("db/normalized_dim_location.csv", encoding = "UTF-8")
nm2uf <- setNames(L$State_Code, strip(L$Location_Name))
ai <- sheet("outputs/py_statistical_results.xlsx", "Annual_Incidence")
regmap <- unique(ai[, .(UF = UF_Code, Region = RC[Region])])
uf_region <- setNames(regmap$Region, regmap$UF)

# ---------------- cases (db, 2016-2026) ----------------
D <- fread("db/normalized_fact_cases.csv")
D <- merge(D, L[, .(Location_ID, UF = State_Code)], by = "Location_ID")
D[, Region := uf_region[UF]]
S_DB <- "db/normalized_fact_cases.csv"
add("n_months", uniqueN(D[, .(Year, Month)]), S_DB)
add("n_ufs", uniqueN(D$UF), S_DB)
for (d in DIS) {
  x <- D[Disease == d]
  add(paste0("cases.", d, ".all"), sum(x$Cases), S_DB)
  add(paste0("cases.", d, ".all_to2025"), sum(x[Year <= 2025]$Cases), S_DB)
  for (y in unique(x$Year)) add(paste0("cases.", d, ".y", y), sum(x[Year == y]$Cases), S_DB)
  by_uf <- x[, .(n = sum(Cases)), by = UF][order(-n)]
  for (i in seq_len(nrow(by_uf))) add(paste0("cases.", d, ".", by_uf$UF[i]), by_uf$n[i], S_DB)
  for (k in 1:6) { add(paste0("rank_cases.", d, ".", k), by_uf$UF[k], S_DB); add(paste0("rank_cases_val.", d, ".", k), by_uf$n[k], S_DB) }
  by_reg <- x[, .(n = sum(Cases)), by = Region]
  for (i in seq_len(nrow(by_reg))) add(paste0("cases.", d, ".", by_reg$Region[i]), by_reg$n[i], S_DB)
  for (r in c("N", "NE", "SE", "S", "CO")) {
    z <- by_uf[UF %in% names(uf_region)[uf_region == r]][order(n)]
    add(paste0("regmin_uf.", d, ".", r), z$UF[1], S_DB); add(paste0("regmin.", d, ".", r), z$n[1], S_DB)
    add(paste0("regmax_uf.", d, ".", r), z$UF[nrow(z)], S_DB); add(paste0("regmax.", d, ".", r), z$n[nrow(z)], S_DB)
  }
}

# ---------------- national / regional annual incidence (Figure 1A source) ----------------
f1 <- sheet("source_data/Figure1.xlsx", "Fig1A_annual_incidence")
S_F1 <- "source_data/Figure1.xlsx / Fig1A_annual_incidence"
for (i in seq_len(nrow(f1))) {
  v <- VC[[f1$Virus[i]]]; g <- RC[[f1$Geography[i]]]
  add(paste0("ann.", v, ".", g, ".", f1$Year[i]), f1[[4]][i], S_F1)
}
# derived: ratios and ranks of national incidence
nat <- function(v, y) as.numeric(f1[Virus == names(VC)[VC == v] & Geography == "Brazil" & Year == y][[4]])
for (d in DIS) {
  yrs <- 2016:2026; vals <- sapply(yrs, function(y) nat(d, y))
  o <- order(-vals)
  add(paste0("natpeak_year.", d), yrs[o[1]], S_F1); add(paste0("natsecond_year.", d), yrs[o[2]], S_F1)
  add(paste0("natthird_year.", d), yrs[o[3]], S_F1)
  add(paste0("natpeak_ratio_second.", d), vals[o[1]] / vals[o[2]], S_F1)
}
r16 <- sapply(2017:2025, function(y) nat("ZIKV", 2016) / nat("ZIKV", y))
add("zika_ratio_min", min(r16), S_F1); add("zika_ratio_max", max(r16), S_F1)
cw <- f1[Virus == "Chikungunya" & Geography != "Brazil"]
cwm <- cw[which.max(cw[[4]])]
add("chik_regmax_region", RC[[cwm$Geography]], S_F1); add("chik_regmax_year", cwm$Year, S_F1); add("chik_regmax_val", cwm[[4]], S_F1)

# ---------------- seasonality (db, complete years 2016-2025) ----------------
S_SEAS <- "db/normalized_fact_cases.csv (2016-2025 pooled by calendar month)"
for (d in DIS) {
  m <- D[Disease == d & Year <= 2025, .(n = sum(Cases)), by = Month][order(Month)]
  for (k in 1:12) add(paste0("seas.", d, ".m", k), m$n[m$Month == k], S_SEAS)
  add(paste0("seas.", d, ".peak_m"), m$Month[which.max(m$n)], S_SEAS)
  add(paste0("seas.", d, ".marapr_mean"), mean(m$n[m$Month %in% 3:4]), S_SEAS)
  h2 <- m[Month >= 7]; add(paste0("seas.", d, ".h2_min"), min(h2$n), S_SEAS); add(paste0("seas.", d, ".h2_max"), max(h2$n), S_SEAS)
  add(paste0("seas.", d, ".h2_min_m"), h2$Month[which.min(h2$n)], S_SEAS)
}

# ---------------- mean annual incidence, Moran, LISA, Mann-Kendall (geo_spatial_stats) ----------------
S_MI <- "outputs/geo_spatial_stats.xlsx / Mean_Incidence"
mi <- sheet("outputs/geo_spatial_stats.xlsx", "Mean_Incidence")
mi[, `:=`(V = VC[Virus], UF = nm2uf[strip(Location_Name)])]
for (d in DIS) {
  z <- mi[V == d][order(-Mean_Inc)]
  for (i in seq_len(nrow(z))) { add(paste0("minc.", d, ".", z$UF[i]), z$Mean_Inc[i], S_MI); add(paste0("rankof.", d, ".", z$UF[i]), i, S_MI) }
  for (k in 1:6) { add(paste0("rank_minc.", d, ".", k), z$UF[k], S_MI); add(paste0("rank_minc_val.", d, ".", k), z$Mean_Inc[k], S_MI) }
}
gm <- sheet("outputs/geo_spatial_stats.xlsx", "Global_Moran")
for (i in seq_len(nrow(gm))) { d <- VC[[gm$Virus[i]]]
  add(paste0("moran.", d, ".I"), gm$I[i], "outputs/geo_spatial_stats.xlsx / Global_Moran")
  add(paste0("moran.", d, ".p"), gm$p_sim[i], "outputs/geo_spatial_stats.xlsx / Global_Moran")
  add(paste0("moran.", d, ".z"), gm$z_sim[i], "outputs/geo_spatial_stats.xlsx / Global_Moran") }
li <- sheet("outputs/geo_spatial_stats.xlsx", "LISA_Clusters"); li[, V := VC[Virus]]
S_LI <- "outputs/geo_spatial_stats.xlsx / LISA_Clusters"
for (d in DIS) for (cat in c("HH", "LL", "HL", "LH")) {
  u <- li[V == d & LISA_Cat == cat]$Abbr
  add(paste0("lisa_n.", d, ".", cat), length(u), S_LI); add(paste0("lisa_names.", d, ".", cat), join_names(u), S_LI)
  uf <- li[V == d & LISA_Cat_FDR == cat]$Abbr
  add(paste0("lisafdr_n.", d, ".", cat), length(uf), S_LI); add(paste0("lisafdr_names.", d, ".", cat), join_names(uf), S_LI)
}
for (i in seq_len(nrow(li))) { k <- paste0("lisa.", li$V[i], ".", li$Abbr[i]); add(paste0(k, ".cat"), li$LISA_Cat[i], S_LI); add(paste0(k, ".p"), li$LISA_p[i], S_LI); add(paste0(k, ".q"), li$q_value[i], S_LI) }
mk <- sheet("outputs/py_statistical_results.xlsx", "Mann_Kendall"); mk[, `:=`(V = VC[Virus], UF = nm2uf[strip(Location_Name)])]
S_MK <- "outputs/py_statistical_results.xlsx / Mann_Kendall"
for (i in seq_len(nrow(mk))) { k <- paste0("mk.", mk$V[i], ".", mk$UF[i])
  add(paste0(k, ".tau"), mk$Tau[i], S_MK); add(paste0(k, ".slope"), mk$Sen_Slope[i], S_MK)
  add(paste0(k, ".p"), mk$p_value[i], S_MK); add(paste0(k, ".q"), mk$q_value[i], S_MK); add(paste0(k, ".trend"), mk$Trend[i], S_MK) }
for (d in DIS) { z <- mk[V == d]
  for (tr in c("increasing", "decreasing")) { u <- z[Trend == tr][order(p_value)]$UF
    add(paste0("mk_n.", d, ".", tr), length(u), S_MK); add(paste0("mk_names.", d, ".", tr), join_names(u), S_MK) }
  add(paste0("mk_minq.", d), min(z$q_value), S_MK); add(paste0("mk_nfdr.", d), sum(z$Significant_FDR %in% TRUE), S_MK)
  add(paste0("mk_nyears.", d), max(z$n_years), S_MK) }

# ---------------- Spearman ----------------
sp <- sheet("outputs/py_statistical_results.xlsx", "Spearman_Lag"); sp[, `:=`(V = VC[Virus], UF = nm2uf[strip(Location_Name)], R = RC[Region])]
S_SP <- "outputs/py_statistical_results.xlsx / Spearman_Lag"
for (d in DIS) for (v in c("Temp", "Rain")) for (l in 0:2) {
  z <- sp[V == d & Variable == v & Lag == l]; k <- paste0("sp.", d, ".", v, ".", l)
  add(paste0(k, ".mean"), mean(z$Rho), S_SP); add(paste0(k, ".nstates"), nrow(z), S_SP)
  add(paste0(k, ".nsig"), sum(z$p_value < 0.05), S_SP); add(paste0(k, ".prop"), mean(z$p_value < 0.05), S_SP)
  add(paste0(k, ".npos"), sum(z$p_value < 0.05 & z$Rho > 0), S_SP); add(paste0(k, ".nneg"), sum(z$p_value < 0.05 & z$Rho < 0), S_SP)
  add(paste0(k, ".nfdr"), sum(z$Significant_FDR %in% TRUE), S_SP)
  zz <- z[order(-Rho)]
  for (i in 1:5) { add(paste0(k, ".top", i, ".uf"), zz$UF[i], S_SP); add(paste0(k, ".top", i, ".rho"), zz$Rho[i], S_SP) }
  for (r in c("N", "NE", "SE", "S", "CO")) add(paste0(k, ".reg.", r), mean(z[R == r]$Rho), S_SP)
  for (i in seq_len(nrow(z))) { add(paste0(k, ".st.", z$UF[i], ".rho"), z$Rho[i], S_SP); add(paste0(k, ".st.", z$UF[i], ".p"), z$p_value[i], S_SP) }
}
# best-|rho| lag per state (counts)
for (d in DIS) for (v in c("Temp", "Rain")) {
  z <- sp[V == d & Variable == v]; b <- z[, .SD[which.max(abs(Rho))], by = UF]
  for (l in 0:2) add(paste0("sp_bestlag.", d, ".", v, ".", l), sum(b$Lag == l), S_SP)
}

# ---------------- GLM ----------------
rd <- function(f) fread(f)
S_GP <- "outputs/glm_negbin_pooled_fe.csv"
pf <- rd("outputs/glm_negbin_pooled_fe.csv"); pp <- rd("outputs/glm_poisson_pooled_fe.csv")
vmap <- c(Dengue = "DENV", Chikungunya = "CHIKV", Zika = "ZIKV")
for (i in which(pf$Term %in% c("Temp_Avg", "Rain_mm"))) {
  d <- vmap[[pf$Virus[i]]]; t <- pf$Term[i]; k <- paste0("glmp.", d, ".", t)
  add(paste0(k, ".irr"), pf$IRR[i], S_GP); add(paste0(k, ".lo"), pf$IRR_CI_L[i], S_GP); add(paste0(k, ".hi"), pf$IRR_CI_U[i], S_GP)
  add(paste0(k, ".p"), pf$p_value[i], S_GP); add(paste0(k, ".coef"), pf$Coef[i], S_GP); add(paste0(k, ".se"), pf$SE[i], S_GP)
  add(paste0("glmp.", d, ".n"), pf$n[i], S_GP); add(paste0("glmp.", d, ".alpha"), pf$alpha[i], S_GP); add(paste0("glmp.", d, ".aic"), pf$AIC[i], S_GP)
  crit <- (log(pf$IRR_CI_U[i]) - log(pf$IRR_CI_L[i])) / (2 * pf$SE[i])
  add(paste0(k, ".crit"), crit, paste0(S_GP, " (implied critical value (ln hi - ln lo)/(2 SE))"))
  if (t == "Rain_mm") for (m in c(10, 100)) {
    add(paste0(k, ".irr", m), exp(m * pf$Coef[i]), paste0(S_GP, " (exp(", m, " x Coef))"))
    add(paste0(k, ".lo", m), exp(m * (pf$Coef[i] - crit * pf$SE[i])), paste0(S_GP, " (exp(", m, " x (Coef - crit x SE)))"))
    add(paste0(k, ".hi", m), exp(m * (pf$Coef[i] + crit * pf$SE[i])), paste0(S_GP, " (exp(", m, " x (Coef + crit x SE)))"))
  }
}
S_PP <- "outputs/glm_poisson_pooled_fe.csv"
for (i in which(pp$Term %in% c("Temp_Avg"))) { d <- vmap[[pp$Virus[i]]]; k <- paste0("glmpois.", d, ".Temp_Avg")
  add(paste0(k, ".irr"), pp$IRR[i], S_PP); add(paste0(k, ".lo"), pp$IRR_CI_L[i], S_PP); add(paste0(k, ".hi"), pp$IRR_CI_U[i], S_PP); add(paste0("glmpois.", d, ".aic"), pp$AIC[i], S_PP) }
# check that the CI is z-based

# per-state and lagged counts
countsig <- function(df, term, src, tag) {
  for (v in names(vmap)) { z <- df[Term == term & Virus == v & !is.na(p_value)]; d <- vmap[[v]]; k <- paste0(tag, ".", d, ".", term)
    add(paste0(k, ".nmodels"), nrow(z), src); add(paste0(k, ".nsig"), sum(z$p_value < 0.05), src)
    add(paste0(k, ".npos"), sum(z$p_value < 0.05 & z$Coef > 0), src); add(paste0(k, ".nneg"), sum(z$p_value < 0.05 & z$Coef < 0), src)
    add(paste0(k, ".nfdr"), sum(z$Significant_FDR %in% TRUE), src)
    zp <- z[p_value < 0.05 & Coef > 0]; add(paste0(k, ".medirr_sigpos"), if (nrow(zp)) median(zp$IRR) else NA_real_, src) }
}
ps <- rd("outputs/glm_negbin_per_state.csv"); lg <- rd("outputs/glm_negbin_lagged.csv")
for (t in c("Temp_Avg", "Rain_mm")) countsig(ps, t, "outputs/glm_negbin_per_state.csv", "glms")
for (t in c("Temp_Avg", "Temp_Lag1", "Temp_Lag2", "Rain_mm", "Rain_Lag1", "Rain_Lag2")) countsig(lg, t, "outputs/glm_negbin_lagged.csv", "glml")
# DLNM
dl <- rd("outputs/2026-10-08/additional/dlnm_summary.csv")
for (i in seq_len(nrow(dl))) { d <- c(Dengue = "DENV", Chikungunya = "CHIKV", Zika = "ZIKV")[[dl$Virus[i]]]
  add(paste0("dlnm.", d, ".opt"), dl$Temp_optimum_C[i], "outputs/2026-10-08/additional/dlnm_summary.csv"); add(paste0("dlnm.", d, ".irr"), dl$IRR_at_optimum[i], "outputs/2026-10-08/additional/dlnm_summary.csv") }

# ---------------- bootstrap ----------------
for (f in c("cases", "incidence")) { b <- rd(sprintf("outputs/bootstrap_ci_95_%s.csv", f))
  for (i in seq_len(nrow(b))) { k <- paste0("boot.", f, ".", b$Disease[i]); s <- sprintf("outputs/bootstrap_ci_95_%s.csv", f)
    add(paste0(k, ".mean"), b$Mean[i], s); add(paste0(k, ".lo"), b$Bootstrap_CI_Lower[i], s); add(paste0(k, ".hi"), b$Bootstrap_CI_Upper[i], s); add(paste0(k, ".n"), b$n[i], s) } }

# ---------------- clinical / demographic (GraphPad tables behind Figures 5, 7, 8) ----------------
f5a <- sheet("source_data/Figure5.xlsx", "Fig5A_age_group_counts"); f5b <- sheet("source_data/Figure5.xlsx", "Fig5B_sex")
S5A <- "source_data/Figure5.xlsx / Fig5A_age_group_counts"; S5B <- "source_data/Figure5.xlsx / Fig5B_sex"
for (v in names(VC)) { d <- VC[[v]]
  a <- f5a[Virus == v, .(n = sum(Cases)), by = Age_group]; tot_known <- sum(a[Age_group != "Ign/Blank"]$n)
  for (i in seq_len(nrow(a))) add(paste0("cl.", d, ".age.", gsub("[^A-Za-z0-9+-]", "", a$Age_group[i])), a$n[i], S5A)
  add(paste0("cl.", d, ".age.known"), tot_known, S5A)
  add(paste0("cl.", d, ".age.20_39"), a[Age_group == "20-39"]$n, S5A); add(paste0("cl.", d, ".age.40_59"), a[Age_group == "40-59"]$n, S5A)
  add(paste0("cl.", d, ".age.20_59"), a[Age_group %in% c("20-39", "40-59")][, sum(n)], S5A)
  s <- f5b[Virus == v, .(n = sum(Count)), by = Category]
  for (i in seq_len(nrow(s))) add(paste0("cl.", d, ".sex.", s$Category[i]), s$n[i], S5B)
  add(paste0("cl.", d, ".sex.total"), sum(s$n), S5B)
  add(paste0("cl.", d, ".sex.ratio"), s[Category == "F"]$n / s[Category == "M"]$n, S5B)
  ym <- f5b[Virus == v & Category %in% c("M", "F"), .(share_m = sum(Count[Category == "M"]) / sum(Count)), by = Year][order(Year)]
  add(paste0("cl.", d, ".malesh_min"), min(ym$share_m), S5B); add(paste0("cl.", d, ".malesh_max"), max(ym$share_m), S5B)
  add(paste0("cl.", d, ".malesh_first"), ym$share_m[1], S5B); add(paste0("cl.", d, ".malesh_last"), ym$share_m[nrow(ym)], S5B)
  add(paste0("cl.", d, ".malesh_minyear"), ym$Year[which.min(ym$share_m)], S5B); add(paste0("cl.", d, ".malesh_maxyear"), ym$Year[which.max(ym$share_m)], S5B)
  add(paste0("cl.", d, ".year_first"), min(s2 <- f5b[Virus == v]$Year), S5B); add(paste0("cl.", d, ".year_last"), max(f5b[Virus == v]$Year), S5B)
}
agg7 <- function(file, sh, tag, vir) {
  z <- sheet(file, sh); a <- z[, .(n = sum(Count)), by = Category]; src <- sprintf("%s / %s", file, sh)
  for (i in seq_len(nrow(a))) add(paste0(tag, ".", gsub("[^A-Za-z0-9]", "", a$Category[i])), a$n[i], src)
  add(paste0(tag, ".total"), sum(a$n), src)
}
agg7("source_data/Figure7.xlsx", "Fig7C_Hospitalization", "cl.DENV.hosp", "Dengue")
agg7("source_data/Figure7.xlsx", "Fig7D_Serotype", "cl.DENV.sero", "Dengue")
agg7("source_data/Figure7.xlsx", "Fig7A_ELISA", "cl.DENV.elisa", "Dengue")
agg7("source_data/Figure7.xlsx", "Fig7B_IgM", "cl.DENV.igm", "Dengue")
agg7("source_data/Figure8.xlsx", "Fig8A1_Chik_Classfic", "cl.CHIKV.class", "Chikungunya")
agg7("source_data/Figure8.xlsx", "Fig8A2_Chik_Criteria", "cl.CHIKV.crit", "Chikungunya")
agg7("source_data/Figure8.xlsx", "Fig8A3_Chik_Evolutio", "cl.CHIKV.evo", "Chikungunya")
agg7("source_data/Figure8.xlsx", "Fig8B1_Zika_Classifi", "cl.ZIKV.class", "Zika")
agg7("source_data/Figure8.xlsx", "Fig8B2_Zika_Criteria", "cl.ZIKV.crit", "Zika")
agg7("source_data/Figure8.xlsx", "Fig8B3_Zika_Evolutio", "cl.ZIKV.evo", "Zika")
agg7("source_data/Figure8.xlsx", "Fig8B4_Zika_Pregnanc", "cl.ZIKV.preg", "Zika")
# serotype share of typed records by year (Figure 7D table), and fully-ignored share
z7 <- sheet("source_data/Figure7.xlsx", "Fig7D_Serotype"); S7D <- "source_data/Figure7.xlsx / Fig7D_Serotype"
for (y in sort(unique(z7$Year))) { zz <- z7[Year == y & Category != "Ign/Blank"]; tt <- sum(zz$Count)
  for (c in c("DENV 1", "DENV 2", "DENV 3", "DENV 4")) add(paste0("cl.DENV.sero_share.", gsub(" ", "", c), ".", y), zz[Category == c]$Count / tt, S7D)
  add(paste0("cl.DENV.sero_typed.", y), tt, S7D) }
# hospitalization share among known
hz <- sheet("source_data/Figure7.xlsx", "Fig7C_Hospitalization")[, .(n = sum(Count)), by = Category]
add("cl.DENV.hosp.share_known", hz[Category == "Positive"]$n / (hz[Category == "Positive"]$n + hz[Category == "Negative"]$n), "source_data/Figure7.xlsx / Fig7C_Hospitalization")
# discard shares in the clinical tables (2016-2025; chikungunya 2017-2025)
dz <- sheet("source_data/Figure8.xlsx", "Fig8B1_Zika_Classifi")[, .(n = sum(Count)), by = Category]
add("cl.ZIKV.disc_share", dz[Category == "Discarded"]$n / sum(dz$n), "source_data/Figure8.xlsx / Fig8B1_Zika_Classifi")
dc <- sheet("source_data/Figure8.xlsx", "Fig8A1_Chik_Classfic")[, .(n = sum(Count)), by = Category]
add("cl.CHIKV.disc_share", dc[Category == "Descarded"]$n / sum(dc$n), "source_data/Figure8.xlsx / Fig8A1_Chik_Classfic")
add("cl.CHIKV.disc", dc[Category == "Descarded"]$n, "source_data/Figure8.xlsx / Fig8A1_Chik_Classfic")
add("cl.CHIKV.conf", dc[Category == "Chikungunya"]$n, "source_data/Figure8.xlsx / Fig8A1_Chik_Classfic")
add("cl.CHIKV.class.all", sum(dc$n), "source_data/Figure8.xlsx / Fig8A1_Chik_Classfic")
add("cl.ZIKV.disc", dz[Category == "Discarded"]$n, "source_data/Figure8.xlsx / Fig8B1_Zika_Classifi")
add("cl.ZIKV.conf", dz[Category == "Confirmed"]$n, "source_data/Figure8.xlsx / Fig8B1_Zika_Classifi")
add("cl.ZIKV.incl", dz[Category == "Inconclusive"]$n, "source_data/Figure8.xlsx / Fig8B1_Zika_Classifi")
add("cl.ZIKV.class.all", sum(dz$n), "source_data/Figure8.xlsx / Fig8B1_Zika_Classifi")

# ---------------- exclusions (figure_exclusions.csv) ----------------
fe <- fread("outputs/figure_exclusions.csv")
S_FE <- "outputs/figure_exclusions.csv"
fe <- fe[as.character(Year) == "All"]
for (spec in list(c("Figure 7C", "Dengue", "hosp"), c("Figure 7D", "Dengue", "sero"), c("Figure 7A", "Dengue", "elisa"), c("Figure 7B", "Dengue", "igm"))) {
  z <- fe[Figure == spec[1] & Virus == spec[2]]
  if (nrow(z)) { add(paste0("fe.DENV.", spec[3], ".total"), sum(z$n_total), S_FE); add(paste0("fe.DENV.", spec[3], ".excl"), sum(z$n_excluded), S_FE)
    add(paste0("fe.DENV.", spec[3], ".valid"), sum(z$n_valid), S_FE); add(paste0("fe.DENV.", spec[3], ".pct"), 100 * sum(z$n_excluded) / sum(z$n_total), S_FE) } }
cat("Figure labels in figure_exclusions:", paste(unique(fe$Figure), collapse = "; "), "\n")

# ---------------- additional families ----------------
S_AI <- "outputs/py_statistical_results.xlsx / Annual_Incidence"
ai[, `:=`(V = VC[Virus], UF = nm2uf[strip(Location_Name)])]
for (i in seq_len(nrow(ai))) add(paste0("ann_state.", ai$V[i], ".", ai$UF[i], ".", ai$Year[i]), ai$Annual_Inc_100k[i], S_AI)
for (d in DIS) for (tr in c("increasing", "decreasing")) { z <- mk[V == d & Trend == tr]
  if (nrow(z)) { add(paste0("mk_taumin.", d, ".", tr), min(z$Tau), S_MK); add(paste0("mk_taumax.", d, ".", tr), max(z$Tau), S_MK)
                 add(paste0("mk_qmin.", d, ".", tr), min(z$q_value), S_MK) } }
psr <- merge(ps[Term == "Temp_Avg" & p_value < 0.05 & Coef > 0], data.table(Location_Name = L$Location_Name, UF = L$State_Code), by = "Location_Name")
psr[, R := uf_region[UF]]
for (d in names(vmap)) for (r in c("N", "NE", "SE", "S", "CO")) add(paste0("glms.", vmap[[d]], ".Temp_Avg.posreg.", r), nrow(psr[Virus == d & R == r]), "outputs/glm_negbin_per_state.csv")
for (i in which(pp$Term == "Temp_Avg")) add(paste0("glmpois.", vmap[[pp$Virus[i]]], ".disp"), pp$dispersion[i], S_PP)
hz2 <- sheet("source_data/Figure7.xlsx", "Fig7C_Hospitalization")[, .(n = sum(Count)), by = Category]
add("cl.DENV.hosp.known", hz2[Category %in% c("Positive", "Negative")][, sum(n)], "source_data/Figure7.xlsx / Fig7C_Hospitalization")
sz2 <- sheet("source_data/Figure7.xlsx", "Fig7D_Serotype")[, .(n = sum(Count)), by = Category]
add("cl.DENV.sero.typed", sz2[Category != "Ign/Blank"][, sum(n)], "source_data/Figure7.xlsx / Fig7D_Serotype")
add("cl.DENV.sero.typed_share", sz2[Category != "Ign/Blank"][, sum(n)] / sum(sz2$n), "source_data/Figure7.xlsx / Fig7D_Serotype")
ct <- fread("clinical_tables/clinical_demographic_long.csv", encoding = "UTF-8")
S_CT <- "clinical_tables/clinical_demographic_long.csv (serotype)"
cts <- ct[Dimension == "serotype" & Disease == "DENV"]
for (y in sort(unique(cts$Year))) { zz <- cts[Year == y]; typ <- zz[Category %in% paste0("DENV", 1:4)]; tt <- sum(typ$Count)
  add(paste0("ct.sero_typed.", y), tt, S_CT); add(paste0("ct.sero_all.", y), sum(zz$Count), S_CT); add(paste0("ct.sero_typed_pct.", y), tt / sum(zz$Count), S_CT)
  for (k in 1:4) { add(paste0("ct.sero_n.DENV", k, ".", y), typ[Category == paste0("DENV", k)]$Count, S_CT); add(paste0("ct.sero_share.DENV", k, ".", y), typ[Category == paste0("DENV", k)]$Count / tt, S_CT) } }
clim <- fread("db/normalized_fact_climate.csv")
add("clim.n_states_2026", uniqueN(clim[Year == 2026 & !is.na(Temp_Avg)]$Location_ID), "db/normalized_fact_climate.csv")
add("clim.rain_mean", mean(clim$Rain_mm, na.rm = TRUE), "db/normalized_fact_climate.csv"); add("clim.rain_sd", sd(clim$Rain_mm, na.rm = TRUE), "db/normalized_fact_climate.csv")
add("clim.temp_mean", mean(clim$Temp_Avg, na.rm = TRUE), "db/normalized_fact_climate.csv"); add("clim.temp_sd", sd(clim$Temp_Avg, na.rm = TRUE), "db/normalized_fact_climate.csv")

add("cl.ZIKV.preg.tri_sum", sum(sheet("source_data/Figure8.xlsx", "Fig8B4_Zika_Pregnanc")[Category %in% c("1º Trimester", "2º Trimester", "3º Trimester")]$Count), "source_data/Figure8.xlsx / Fig8B4_Zika_Pregnanc")
for (y in sort(unique(cts$Year))) add(paste0("ct.sero_code0.", y), sum(cts[Year == y & Category == "codigo_0"]$Count), S_CT)
er <- fread("outputs/2026-10-08/additional/dlnm_exposure_response.csv", encoding = "UTF-8")
add("dlnm.ref.Temp", unique(er[Predictor == "Temp"]$Reference)[1], "outputs/2026-10-08/additional/dlnm_exposure_response.csv")

for (d in DIS) for (tr in c("increasing", "decreasing")) { z <- mk[V == d & Trend == tr][order(p_value)]
  for (i in seq_len(nrow(z))) { k <- paste0("mkr.", d, ".", tr, ".", i)
    add(paste0(k, ".uf"), z$UF[i], S_MK); add(paste0(k, ".tau"), z$Tau[i], S_MK); add(paste0(k, ".slope"), z$Sen_Slope[i], S_MK); add(paste0(k, ".p"), z$p_value[i], S_MK); add(paste0(k, ".q"), z$q_value[i], S_MK) } }
for (d in DIS) for (cat in c("HH", "LL", "HL", "LH")) add(paste0("lisa_uf.", d, ".", cat), paste(li[V == d & LISA_Cat == cat]$Abbr, collapse = ","), S_LI)

D2 <- D[, .(n = sum(Cases)), by = .(Disease, UF)][order(Disease, -n)]
for (d in DIS) for (k in 1:2) { uf <- D2[Disease == d]$UF[k]
  add(paste0("rank_of_topcases.", d, ".", k), mi[V == d & UF == uf][order(-Mean_Inc)][, .I][1] * 0 + which(mi[V == d][order(-Mean_Inc)]$UF == uf), "outputs/geo_spatial_stats.xlsx / Mean_Incidence (rank of the state with the k-th largest case total)") }
add("cl.DENV.age.20_59_share", as.numeric(sheet("source_data/Figure5.xlsx", "Fig5A_age_group_counts")[Virus == "Dengue" & Age_group %in% c("20-39", "40-59"), sum(Cases)]) / as.numeric(sheet("source_data/Figure5.xlsx", "Fig5A_age_group_counts")[Virus == "Dengue" & Age_group != "Ign/Blank", sum(Cases)]), S5A)

for (d in DIS) { m <- D[Disease == d & Year <= 2025, .(n = sum(Cases)), by = Month]
  add(paste0("seas.", d, ".q4_share"), sum(m[Month >= 10]$n) / sum(m$n), S_SEAS) }
tp <- sapply(2016:2025, function(y) tail(ct[Dimension == "serotype" & Disease == "DENV" & Year == y & Category %in% paste0("DENV", 1:4), sum(Count)], 1) / ct[Dimension == "serotype" & Disease == "DENV" & Year == y, sum(Count)])
add("ct.sero_typed_pct_min", min(tp), S_CT); add("ct.sero_typed_pct_max", max(tp), S_CT)
fe_all <- fread("outputs/figure_exclusions.csv")
for (spec in list(c("Figure 7A", "elisa"), c("Figure 7B", "igm"))) { z <- fe_all[Figure == spec[1] & Virus == "Dengue" & as.character(Year) == "2025"]
  if (nrow(z)) add(paste0("fe.DENV.", spec[2], ".pct2025"), z$pct_excluded[1], "outputs/figure_exclusions.csv")
  z2 <- fe_all[Figure == spec[1] & Virus == "Dengue" & as.character(Year) %in% as.character(2016:2024)]
  add(paste0("fe.DENV.", spec[2], ".pctmin1624"), min(z2$pct_excluded), "outputs/figure_exclusions.csv"); add(paste0("fe.DENV.", spec[2], ".pctmax1624"), max(z2$pct_excluded), "outputs/figure_exclusions.csv") }

# ---------------- write ----------------
out <- rbindlist(rows); setnames(out, "id", "key")
fwrite(out, OUTF)
cat(nrow(out), "keys written to", OUTF, "\n")
