import joblib, json, numpy as np
m = joblib.load('models/random_forest.pkl')
with open('models/metadata.json') as f:
    meta=json.load(f)
cols=meta['feature_columns']
if hasattr(m,'feature_importances_'):
    imp = m.feature_importances_
    idx = np.argsort(imp)[::-1][:5]
    out=[(cols[i], float(imp[i])) for i in idx]
    print(json.dumps(out))
else:
    print('[]')
