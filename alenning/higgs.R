# Higgs Boson data

library(torch)
library(tabnet)
library(tidyverse)
library(tidymodels)
library(finetune) # to use tuning functions from the new finetune package
library(vip) # to plot feature importances
library(sparklyr)

conf <- spark_config()
sc <- spark_connect(master = "spark://10.28.53.201:7077", config = conf, version = '3.0.0-preview2')

set.seed(777)
torch_manual_seed(777)


#Load Dataset
higgs <- read_csv(
  "../pdotson/data/HIGGS.csv",
  col_names = c("class", "lepton_pT", "lepton_eta", "lepton_phi", "missing_energy_magnitude",
                "missing_energy_phi", "jet_1_pt", "jet_1_eta", "jet_1_phi", "jet_1_b_tag",
                "jet_2_pt", "jet_2_eta", "jet_2_phi", "jet_2_b_tag", "jet_3_pt", "jet_3_eta",
                "jet_3_phi", "jet_3_b_tag", "jet_4_pt", "jet_4_eta", "jet_4_phi", "jet_4_b_tag",
                "m_jj", "m_jjj", "m_lv", "m_jlv", "m_bb", "m_wbb", "m_wwbb"),
  col_types = "fdddddddddddddddddddddddddddd"
)

higgs <- copy_to(sc, higgs)

#glimpse data
higgs %>% glimpse()


#split data into train/test
n <- 11000000
n_test <- 500000
test_frac <- n_test/n

split <- initial_time_split(higgs, prop = 1 - test_frac)
train <- training(split)
test  <- testing(split)


#predict class from all other features
rec <- recipe(class ~ ., train) 


# hyperparameter settings (apart from epochs) as per the TabNet paper (TabNet-S)
mod <- tabnet(epochs = 3, batch_size = 16384, decision_width = 24, attention_width = 26,
              num_steps = 5, penalty = 0.000001, virtual_batch_size = 512, momentum = 0.6,
              feature_reusage = 1.5, learn_rate = 0.02) %>%
  set_engine("torch", verbose = TRUE) %>%
  set_mode("classification")


wf <- workflow() %>%
  add_model(mod) %>%
  add_recipe(rec)


fitted_model <- wf %>% fit(train)


# access the underlying parsnip model and save it to RDS format
# depending on when you read this, a nice wrapper may exist
# see https://github.com/mlverse/tabnet/issues/27  
fitted_model$fit$fit$fit %>% saveRDS("saved_model.rds")


preds <- test %>% 
	  bind_cols(predict(fitted_model, test))

  yardstick::accuracy(preds, class, .pred_class)


