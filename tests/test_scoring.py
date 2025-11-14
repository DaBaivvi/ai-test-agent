from agent.models import Protocol, Evidence
from agent.scoring import compute_scores

PROTO = Protocol(protocol_id="wm.v1", category="Waschmaschinen", version=1, criteria=[
    {"id":"energy","name":"Energie","weight":0.5,"rule":{"scale":"lower_better","min":0.0,"max":1.0}},
    {"id":"clean","name":"Reinigung","weight":0.5,"rule":{"scale":"higher_better","min":0.0,"max":1.0}},
])

EVID = Evidence(category="Waschmaschinen", model="X", sources=[], metrics={
    "energy_kwh_per_cycle":0.4,
    "clean_index":0.8,
})

def test_total_in_01():
    s = compute_scores(PROTO, EVID)
    assert 0.0 <= s.total <= 1.0
