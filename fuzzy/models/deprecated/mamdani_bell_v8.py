from simpful import FuzzySystem, LinguisticVariable, FuzzySet, TriangleFuzzySet
from fuzzy.models.bell_mf import Bell_MF
from fuzzy.fuzzy_system_wrapper import FuzzySystemWrapper


FS = FuzzySystemWrapper()


# Memory Usage Avg [%]
M1 = FuzzySet(function=Bell_MF(a=4, b=0.5, c=0), term="very_low")
M2 = FuzzySet(function=Bell_MF(a=4, b=0.05, c=0.5), term="low")
M3 = FuzzySet(function=Bell_MF(a=2, b=0.1, c=0.65), term="medium")
M4 = FuzzySet(function=Bell_MF(a=2, b=0.05, c=0.8), term="high")
M5 = TriangleFuzzySet(0.8, 1, 1, term="very_high")

FS.add_linguistic_variable("SystemLoad", LinguisticVariable([M1,M2,M3, M4, M5], universe_of_discourse=[0,1]))

# Latency
L1 = FuzzySet(function=Bell_MF(a=4, b=0.7, c=0), term="low")
L2 = FuzzySet(function=Bell_MF(a=4, b=0.2, c=1), term="high")
FS.add_linguistic_variable("Latency", LinguisticVariable([L1, L2], universe_of_discourse=[0,1]))

# CLP Variation (output)
CLP1 = TriangleFuzzySet(-1, -1, -0.7, term="decrease_significantly")
CLP2 = FuzzySet(function=Bell_MF(a=2, b=0.05, c=-0.75), term="decrease")
CLP3 = FuzzySet(function=Bell_MF(a=1, b=0.1, c=0.1), term="maintain")
CLP4 = FuzzySet(function=Bell_MF(a=2, b=0.05, c=0.5), term="increase")
CLP5 = TriangleFuzzySet(0.7, 1, 1, term="increase_significantly")
#CLP5 = FuzzySet(function=Bell_MF(a=2, b=0.15, c=1), term="increase_significantly")
FS.add_linguistic_variable("CLP", LinguisticVariable([CLP1, CLP2, CLP3, CLP4, CLP5], universe_of_discourse=[-1,1]))

FS.add_rules([
    "IF (SystemLoad IS low) THEN (CLP IS increase)",
    "IF (SystemLoad IS medium) THEN (CLP IS maintain)",
    "IF (SystemLoad IS high) THEN (CLP IS decrease)",
    "IF (SystemLoad IS very_low) THEN (CLP IS increase_significantly)",
    "IF (SystemLoad IS very_high) OR (Latency IS high) THEN (CLP IS decrease_significantly)",
])

if __name__ == '__main__':
    import os
    import pickle
    from fuzzy.visualization import *

    save_path = '../../output/deprecated/mamdani_bell_v8'

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    plot_inputs_outputs_fuzzy_system(FS, save_path)
    #plot_memory_processor_clp(FS, save_path)

    with open(f"{save_path}/model.pkl", "wb") as f:
        pickle.dump(FS, f)
