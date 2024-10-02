from simpful import FuzzySystem, LinguisticVariable, FuzzySet
from fuzzy.models.bell_mf import Bell_MF

FS = FuzzySystem()


# Memory Usage Avg [%]
M1 = FuzzySet(function=Bell_MF(a=4, b=0.7, c=0), term="low")
M2 = FuzzySet(function=Bell_MF(a=2, b=0.1, c=0.7), term="medium")
M3 = FuzzySet(function=Bell_MF(a=2, b=0.2, c=1), term="high")
FS.add_linguistic_variable("SystemLoad", LinguisticVariable([M1,M2,M3], universe_of_discourse=[0,1]))

# CLP Variation (output)
CLP3 = FuzzySet(function=Bell_MF(a=2, b=0.4, c=-1), term="decrease")
CLP2 = FuzzySet(function=Bell_MF(a=2, b=0.05, c=0), term="maintain")
CLP1 = FuzzySet(function=Bell_MF(a=2, b=0.4, c=1), term="increase")
FS.add_linguistic_variable("CLP", LinguisticVariable([CLP1, CLP2, CLP3], universe_of_discourse=[-1,1]))

FS.add_rules([
    "IF (SystemLoad IS low) THEN (CLP IS increase)",
    "IF (SystemLoad IS medium) THEN (CLP IS maintain)",
    "IF (SystemLoad IS high) THEN (CLP IS decrease)",
])

if __name__ == '__main__':
    import os
    import pickle
    from fuzzy.visualization import *

    save_path = '../output/mamdani_bell_v2'

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    plot_inputs_outputs_fuzzy_system(FS, save_path)
    #plot_memory_processor_clp(FS, save_path)

    with open(f"{save_path}/model.pkl", "wb") as f:
        pickle.dump(FS, f)