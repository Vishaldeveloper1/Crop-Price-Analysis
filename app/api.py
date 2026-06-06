import pandas as pd

# =====================================
# LOAD AGRICULTURE DATASET
# =====================================

df = pd.read_csv(
    "data/Agriculture_price_dataset.csv"
)

# =====================================
# CLEAN COLUMN NAMES
# =====================================

df.columns = df.columns.str.strip()

# =====================================
# RENAME COLUMNS
# =====================================

df.rename(columns={
    'STATE': 'state',
    'District Name': 'district',
    'Market Name': 'market',
    'Commodity': 'commodity',
    'Min_Price': 'min_price',
    'Max_Price': 'max_price',
    'Modal_Price': 'modal_price'
}, inplace=True)

# =====================================
# GET STATES
# =====================================

def get_states():

    return sorted(
        df['state']
        .dropna()
        .unique()
    )

# =====================================
# GET DISTRICTS
# =====================================

def get_districts(state):

    filtered = df[
        df['state'] == state
    ]

    return sorted(
        filtered['district']
        .dropna()
        .unique()
    )

# =====================================
# GET MANDI DATA
# =====================================

def get_mandi_data(state, district):

    filtered = df[
        (df['state'] == state)
        &
        (df['district'] == district)
    ]

    return filtered