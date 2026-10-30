from pathlib import Path
import numpy as np
import pandas as pd
import zipfile
import json

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
DATA.mkdir(exist_ok=True)
rng = np.random.default_rng(20261020)

# ---------- small helpers ----------
def choice(values, size=None, p=None, replace=True):
    return rng.choice(values, size=size, p=p, replace=replace)
def rand_dates(start, end, n):
    start = np.datetime64(start, 'D'); end = np.datetime64(end, 'D')
    days = int((end - start).astype(int))
    return start + rng.integers(0, days + 1, size=n).astype('timedelta64[D]')
def write(df, name):
    df.to_csv(DATA / name, index=False, date_format='%Y-%m-%dT%H:%M:%S')

# ---------- customers ----------
first_names = ['Aarav','Aanya','Aditi','Aditya','Ahmed','Akash','Alisha','Ananya','Arjun','Diya','Farhan','Fatima','Isha','Kabir','Karan','Kavya','Meera','Mira','Mohammed','Neha','Nikhil','Priya','Rahul','Riya','Rohan','Sana','Sara','Shreya','Tanya','Varun','Zoya','Ibrahim','Noor','Dev','Ishaan','Anika','Vikram','Simran','Pooja','Yusuf']
last_names = ['Sharma','Verma','Singh','Khan','Patel','Gupta','Kumar','Das','Mehta','Joshi','Rao','Malik','Kapoor','Bose','Iyer','Nair','Chopra','Bhat','Ali','Saxena','Gill','Reddy','Mishra','Sethi','Dutta','Ansari','Thomas','Sheikh','Menon','Shah']
city_state = {
    'Delhi':'Delhi','Mumbai':'Maharashtra','Pune':'Maharashtra','Nagpur':'Maharashtra','Bengaluru':'Karnataka','Mysuru':'Karnataka','Chennai':'Tamil Nadu','Coimbatore':'Tamil Nadu','Hyderabad':'Telangana','Warangal':'Telangana','Kolkata':'West Bengal','Siliguri':'West Bengal','Jaipur':'Rajasthan','Jodhpur':'Rajasthan','Lucknow':'Uttar Pradesh','Varanasi':'Uttar Pradesh','Chandigarh':'Chandigarh','Ludhiana':'Punjab','Amritsar':'Punjab','Kathua':'Jammu and Kashmir','Jammu':'Jammu and Kashmir','Srinagar':'Jammu and Kashmir','Ahmedabad':'Gujarat','Surat':'Gujarat','Kochi':'Kerala','Thiruvananthapuram':'Kerala','Bhopal':'Madhya Pradesh','Indore':'Madhya Pradesh','Bhubaneswar':'Odisha','Guwahati':'Assam'
}
cities = list(city_state.keys()); city_probs = np.array([1.3 if c in ['Delhi','Mumbai','Bengaluru','Chennai','Hyderabad','Kolkata'] else 1.0 for c in cities]); city_probs /= city_probs.sum()
n_cust = 800
customer_ids = [f'C{i:05d}' for i in range(1,n_cust+1)]
c_city = choice(cities, n_cust, p=city_probs)
cust = pd.DataFrame({
    'customer_id': customer_ids,
    'customer_name': [f'{choice(first_names)} {choice(last_names)}' for _ in range(n_cust)],
    'age': rng.integers(18, 76, n_cust),
    'gender': choice(['Female','Male','Non-binary','Prefer not to say'], n_cust, p=[.47,.48,.02,.03]),
    'city': c_city,
    'state': [city_state[c] for c in c_city],
    'signup_date': rand_dates('2018-01-01','2022-12-31', n_cust),
    'acquisition_channel': choice(['Organic Search','Social Media','Referral','Paid Search','Email','Direct'], n_cust, p=[.24,.19,.15,.18,.12,.12]),
    'loyalty_tier': choice(['Bronze','Silver','Gold','Platinum'], n_cust, p=[.43,.31,.19,.07]),
    'is_active': choice([True,False], n_cust, p=[.87,.13]),
    'satisfaction_score': rng.choice([1,2,3,4,5,np.nan], n_cust, p=[.035,.07,.19,.36,.30,.045]),
    'referral_code': [None if x else f'REF{int(rng.integers(1000,9999))}' for x in rng.random(n_cust) < .72],
})
# Ensure dtype-friendly columns
cust['age'] = cust['age'].astype('int64')
write(cust, 'customers.csv')

# ---------- products ----------
product_templates = {
    'Electronics': ['Wireless Earbuds','Bluetooth Speaker','USB-C Hub','Power Bank','Desk Lamp','Mechanical Keyboard','Webcam','Smart Watch','Portable SSD','Phone Stand','Noise-Canceling Headphones','Charging Cable'],
    'Home': ['Cotton Bedsheet','Ceramic Mug Set','Storage Basket','Water Bottle','Table Organizer','Cotton Towel Set','Floor Lamp','Glass Food Containers','Cushion Cover','Laundry Hamper'],
    'Grocery': ['Green Tea Pack','Coffee Beans','Olive Oil','Trail Mix','Oats Pack','Dark Chocolate','Peanut Butter','Pasta Pack','Spice Box','Honey Jar'],
    'Fashion': ['Everyday T-Shirt','Denim Jeans','Canvas Backpack','Running Cap','Cotton Kurta','Sneakers','Leather Belt','Winter Scarf','Sports Socks','Casual Shirt'],
    'Sports': ['Yoga Mat','Resistance Bands','Skipping Rope','Insulated Shaker','Dumbbell Pair','Tennis Balls','Cycling Gloves','Football','Gym Towel','Hiking Bottle'],
    'Books': ['Data Science Handbook','Python Practice Guide','Mystery Novel','World History Atlas','Statistics Workbook','Science Encyclopedia','Classic Short Stories','Personal Finance Guide'],
    'Beauty': ['Face Moisturizer','Sunscreen Lotion','Shampoo Bottle','Hand Cream','Cleansing Gel','Hair Oil','Lip Balm','Bath Essentials Set']
}
base_price = {'Electronics': (350,18000),'Home':(180,4500),'Grocery':(80,1600),'Fashion':(250,6000),'Sports':(200,8000),'Books':(180,1800),'Beauty':(100,2200)}
subcats = {
    'Electronics':['Audio','Accessories','Computing','Wearables'], 'Home':['Bedroom','Kitchen','Storage','Decor'],
    'Grocery':['Beverages','Pantry','Snacks'], 'Fashion':['Clothing','Footwear','Accessories'],
    'Sports':['Fitness','Outdoor','Team Sports'], 'Books':['Technology','Education','Fiction','Reference'],
    'Beauty':['Skin Care','Hair Care','Personal Care']}
n_prod = 150
p_categories = choice(list(product_templates), n_prod)
prod_rows=[]
for i, cat in enumerate(p_categories,1):
    lo, hi = base_price[cat]
    price = float(np.round(np.exp(rng.uniform(np.log(lo), np.log(hi))),2))
    prefix = choice(['Everyday','Premium','Classic','Compact','Essential','Pro','Eco','Urban'])
    prod_rows.append({
        'product_id':f'P{i:04d}',
        'product_name':f'{prefix} {choice(product_templates[cat])}',
        'category':cat,
        'subcategory':choice(subcats[cat]),
        'brand':choice(['Northstar','Blue Fern','DailyPeak','Mango Grove','Orbit Works','Cedar & Co.','NovaField','Brightline']),
        'unit_cost':round(price*rng.uniform(.42,.74),2),
        'list_price':price,
        'weight_kg':round(float(np.exp(rng.uniform(np.log(.03),np.log(8)))),3),
        'stock_target':int(rng.integers(15,220)),
        'launch_date':rand_dates('2020-01-01','2026-06-30',1)[0],
        'discontinued':bool(rng.random()<.08),
        'customer_rating':rng.choice([1,2,3,4,5,np.nan],p=[.02,.05,.16,.39,.32,.06]),
    })
products = pd.DataFrame(prod_rows)
write(products, 'products.csv')

# ---------- orders and line items ----------
n_orders = 3200
order_ids = [f'O{i:06d}' for i in range(1,n_orders+1)]
order_dates = pd.to_datetime(rand_dates('2023-01-01','2026-09-30',n_orders))
# Choose customers, weighted slightly toward more recent signups / active users
cust_weights = np.where(cust['is_active'].to_numpy(), 1.25, .5).astype(float); cust_weights /= cust_weights.sum()
order_customers = choice(customer_ids,n_orders,p=cust_weights)
status = choice(['Delivered','Shipped','Processing','Cancelled','Returned'], n_orders,p=[.68,.12,.09,.07,.04])
channel = choice(['Website','Mobile App','Marketplace','Retail Partner'],n_orders,p=[.42,.31,.19,.08])
payment = choice(['UPI','Credit Card','Debit Card','Net Banking','Cash on Delivery','Wallet'],n_orders,p=[.35,.20,.16,.11,.12,.06])
order_rows=[]; item_rows=[]; item_counter=1
product_ix = products.set_index('product_id')
for idx, oid in enumerate(order_ids):
    od = order_dates[idx]
    st = status[idx]
    n_lines = int(rng.choice([1,2,3,4,5],p=[.25,.32,.22,.14,.07]))
    selected = choice(products['product_id'].to_numpy(),n_lines,replace=False)
    line_sum = 0.0; cost_sum = 0.0
    for pid in selected:
        pr = product_ix.loc[pid]
        qty = int(rng.choice([1,2,3,4,5],p=[.53,.25,.13,.065,.025]))
        disc = float(rng.choice([0,.05,.10,.15,.20,.25],p=[.38,.18,.20,.12,.08,.04]))
        unit_price = round(float(pr['list_price'])*float(rng.uniform(.94,1.04)),2)
        gross = round(qty*unit_price,2); discount_amt = round(gross*disc,2); net = round(gross-discount_amt,2)
        line_sum += net; cost_sum += qty*float(pr['unit_cost'])
        item_rows.append({'order_item_id':f'LI{item_counter:07d}','order_id':oid,'product_id':pid,'quantity':qty,'unit_price':unit_price,'discount_pct':disc,'gross_amount':gross,'discount_amount':discount_amt,'net_sales':net,'estimated_cost':round(qty*float(pr['unit_cost']),2),'is_returned':bool(st=='Returned' or rng.random()<.015)})
        item_counter+=1
    ship_fee = round(float(rng.choice([0,35,50,70,90,120],p=[.16,.18,.26,.20,.13,.07])),2)
    tax_rate = float(rng.choice([.05,.12,.18],p=[.25,.30,.45]))
    tax_amt = round(line_sum*tax_rate,2)
    total = round(line_sum + ship_fee + tax_amt,2)
    ship_days = int(rng.integers(1,5))
    ship_date = (od + pd.Timedelta(days=int(rng.integers(0,3)))) if st in ['Delivered','Shipped','Returned'] else pd.NaT
    delivery_date = (ship_date + pd.Timedelta(days=ship_days)) if st in ['Delivered','Returned'] else pd.NaT
    promised = od + pd.Timedelta(days=5)
    delay = (delivery_date-promised).days if pd.notna(delivery_date) else np.nan
    custrow = cust.loc[cust['customer_id']==order_customers[idx]].iloc[0]
    order_rows.append({'order_id':oid,'customer_id':order_customers[idx],'order_date':od,'ship_date':ship_date,'delivery_date':delivery_date,'promised_delivery_date':promised,'delivery_delay_days':delay,'order_status':st,'sales_channel':channel[idx],'payment_method':payment[idx],'shipping_city':custrow['city'],'shipping_state':custrow['state'],'shipping_fee':ship_fee,'tax_rate':tax_rate,'tax_amount':tax_amt,'items_net_sales':round(line_sum,2),'order_total':total,'estimated_cost':round(cost_sum,2)})
orders = pd.DataFrame(order_rows)
items = pd.DataFrame(item_rows)
# Set consistent pandas date strings
write(orders, 'orders.csv')
write(items, 'order_items.csv')
# Wide single-file table for immediate practice, without needing joins first.
transactions = (items.merge(orders, on='order_id', how='left', validate='many_to_one')
                .merge(products, on='product_id', how='left', validate='many_to_one')
                .merge(cust.drop(columns=['city','state']), on='customer_id', how='left', validate='many_to_one', suffixes=('','_customer')))
write(transactions, 'retail_transactions.csv')

# ---------- website events ----------
n_events = 18000
event_ids=[f'E{i:07d}' for i in range(1,n_events+1)]
base_ts=pd.Timestamp('2023-01-01').value
end_ts=pd.Timestamp('2026-10-01').value
ts = pd.to_datetime(rng.integers(base_ts,end_ts,n_events))
event_type=choice(['page_view','product_view','search','add_to_cart','checkout_start','purchase','review_submit','support_open'],n_events,p=[.31,.24,.12,.12,.075,.045,.035,.055])
web = pd.DataFrame({
    'event_id':event_ids,
    'event_timestamp':ts,
    'customer_id':[None if x else choice(customer_ids) for x in (rng.random(n_events)<.30)],
    'session_id':[f'S{int(x):07d}' for x in rng.integers(1, int(n_events*.72), n_events)],
    'event_type':event_type,
    'page_category':choice(['Home','Search Results','Product Detail','Category','Cart','Checkout','Help','Reviews'],n_events),
    'device':choice(['Android','iOS','Windows','macOS','Other'],n_events,p=[.32,.19,.25,.18,.06]),
    'traffic_source':choice(['Organic','Paid Search','Social','Referral','Email','Direct'],n_events,p=[.27,.17,.19,.12,.12,.13]),
    'campaign_id':[None if x else f'CAM{int(rng.integers(1,31)):03d}' for x in (rng.random(n_events)<.58)],
    'duration_seconds':np.where(event_type=='purchase',rng.integers(10,180,n_events),rng.integers(1,900,n_events)),
    'items_in_cart':rng.integers(0,8,n_events),
    'event_revenue':np.where(event_type=='purchase',np.round(np.exp(rng.normal(6.4,1.0,n_events)),2),0),
    'converted':event_type=='purchase',
})
write(web, 'website_events.csv')

# ---------- regional daily metrics for datetime, rolling and resampling ----------
days=pd.date_range('2023-01-01','2026-09-30',freq='D')
regions=['North','South','East','West']
metric_rows=[]
for region in regions:
    region_scale={'North':1.15,'South':1.0,'East':.78,'West':1.20}[region]
    for d in days:
        if rng.random()<.012:  # intentional missing dates for resampling / reindexing practice
            continue
        yearly=1 + .18*np.sin(2*np.pi*(d.dayofyear/365.25))
        weekend=1.17 if d.dayofweek>=5 else 1.0
        festive=1.55 if d.month in [10,11] else 1.0
        visits=max(20,int(rng.normal(950*region_scale*yearly*weekend*festive,140*region_scale)))
        conv=float(np.clip(rng.normal(.032 + (.005 if d.dayofweek>=5 else 0),.009),.004,.09))
        orders_n=int(max(0,visits*conv))
        aov=float(np.clip(rng.normal(1450,350),350,4200))
        revenue=round(orders_n*aov,2)
        ad_spend=round(max(0,rng.normal(visits*.85,visits*.18)),2)
        returns_n=int(rng.binomial(max(orders_n,1),.045))
        metric_rows.append({'date':d,'region':region,'visits':visits,'orders':orders_n,'conversion_rate':round(orders_n/visits if visits else 0,5),'average_order_value':round(aov,2),'revenue':revenue,'ad_spend':ad_spend,'returns':returns_n,'new_customers':int(rng.binomial(max(orders_n,1),.31)),'marketing_campaign':choice(['None','Festive Sale','Payday Offer','Weekend Boost','New Launch'],p=[.48,.17,.13,.12,.10])})
daily = pd.DataFrame(metric_rows)
write(daily, 'daily_regional_metrics.csv')

# ---------- inventory movements ----------
n_moves=5200
move_types=choice(['Restock','Sale','Customer Return','Damage','Transfer In','Transfer Out','Stock Correction'],n_moves,p=[.20,.44,.06,.035,.09,.09,.085])
move_qty=[]
for t in move_types:
    if t in ['Restock','Customer Return','Transfer In']:
        q=int(rng.integers(1,101))
    elif t in ['Sale','Transfer Out']:
        q=-int(rng.integers(1,13))
    elif t=='Damage':
        q=-int(rng.integers(1,8))
    else:
        q=int(rng.integers(-15,16))
    move_qty.append(q)
inv_product_ids = choice(products['product_id'].to_numpy(), n_moves)
inv = pd.DataFrame({
    'movement_id':[f'M{i:06d}' for i in range(1,n_moves+1)],
    'movement_date':pd.to_datetime(rand_dates('2023-01-01','2026-09-30',n_moves)),
    'product_id':inv_product_ids,
    'warehouse_id':choice(['WH-NORTH','WH-SOUTH','WH-EAST','WH-WEST'],n_moves),
    'movement_type':move_types,
    'quantity_change':move_qty,
    'unit_cost': [round(float(product_ix.loc[p,'unit_cost']),2) for p in inv_product_ids],
    'reference_type':choice(['Order','Supplier PO','Manual Adjustment','Return Ticket','Transfer'],n_moves),
    'notes':choice(['routine movement','cycle count','supplier delivery','damaged item','customer return','inter-warehouse transfer','promotion stock'],n_moves),
})
write(inv, 'inventory_movements.csv')

# ---------- employees: groupby/agg, dates, rankings, correlation ----------
n_emp=140
emp_ids=[f'EMP{i:04d}' for i in range(1,n_emp+1)]
depts=['Analytics','Engineering','Marketing','Sales','Operations','Customer Support','Finance','Human Resources']
emp_dep=choice(depts,n_emp,p=[.12,.20,.13,.19,.16,.10,.06,.04])
role_map={'Analytics':['Data Analyst','Senior Analyst','Analytics Lead'],'Engineering':['Python Developer','Software Engineer','QA Engineer','Engineering Lead'],'Marketing':['Campaign Executive','Content Specialist','Marketing Manager'],'Sales':['Sales Associate','Account Executive','Sales Manager'],'Operations':['Operations Associate','Supply Planner','Operations Lead'],'Customer Support':['Support Associate','Support Specialist','Support Lead'],'Finance':['Accountant','Financial Analyst'],'Human Resources':['HR Associate','Recruiter']}
emp_rows=[]
for i,d in enumerate(emp_dep):
    hire=rand_dates('2016-01-01','2026-05-31',1)[0]
    level=choice(['Junior','Mid','Senior'],p=[.43,.39,.18])
    salary_base={'Junior':420000,'Mid':720000,'Senior':1150000}[level]
    emp_rows.append({'employee_id':emp_ids[i],'employee_name':f'{choice(first_names)} {choice(last_names)}','department':d,'job_title':choice(role_map[d]),'level':level,'hire_date':hire,'salary_inr':int(max(280000,rng.normal(salary_base, salary_base*.19))), 'weekly_hours':int(np.clip(rng.normal(41,4),25,60)),'performance_score':round(float(np.clip(rng.normal(3.5,.8),1,5)),1),'work_mode':choice(['Office','Hybrid','Remote'],p=[.38,.46,.16]),'employment_status':choice(['Active','Active','Active','On Leave','Left'],p=[.78,.07,.06,.04,.05]),'bonus_pct':round(float(choice([0,.03,.05,.08,.12,.15],p=[.24,.18,.24,.18,.11,.05])),2),'manager_id':None})
employees=pd.DataFrame(emp_rows)
# Assign managers at department-level where possible; a manager can manage multiple employees.
for d in depts:
    ids=employees.index[employees.department==d].tolist()
    if len(ids)>1:
        manager_ix=ids[0]
        for ix in ids[1:]:
            if rng.random()<.78:
                employees.loc[ix,'manager_id']=employees.loc[manager_ix,'employee_id']
write(employees, 'employees.csv')

# ---------- survey responses: ordinal/categorical/numeric/text ----------
n_surv=1800
comments=['quick delivery and good packaging','price could be better','excellent product quality','easy to use website','support team was helpful','item arrived later than expected','good value for money','packaging had too much plastic','will recommend to friends','product differed slightly from photos','checkout was confusing','great experience overall','size was not as expected','delivery updates were useful','repeat customer and very satisfied']
survey = pd.DataFrame({
    'response_id':[f'R{i:06d}' for i in range(1,n_surv+1)],
    'customer_id':[None if x else choice(customer_ids) for x in (rng.random(n_surv)<.08)],
    'response_date':pd.to_datetime(rand_dates('2023-01-01','2026-09-30',n_surv)),
    'nps_score':rng.choice(list(range(11))+[np.nan],n_surv,p=[.025,.025,.025,.035,.05,.07,.10,.14,.19,.19,.10,.05]),
    'product_quality':rng.choice([1,2,3,4,5,np.nan],n_surv,p=[.025,.055,.15,.39,.33,.05]),
    'delivery_experience':rng.choice([1,2,3,4,5,np.nan],n_surv,p=[.04,.08,.17,.36,.29,.06]),
    'support_experience':rng.choice([1,2,3,4,5,np.nan],n_surv,p=[.025,.05,.12,.24,.25,.315]),
    'would_recommend':choice(['Definitely','Probably','Not sure','Probably not'],n_surv,p=[.49,.31,.14,.06]),
    'comment':choice(comments,n_surv),
    'survey_channel':choice(['Email','SMS','In-App','Website'],n_surv,p=[.33,.18,.39,.10]),
})
write(survey, 'survey_responses.csv')

# ---------- purposely messy table for cleaning exercises ----------
n_dirty=320
raw_dates = [str(pd.Timestamp(x).date()) for x in rand_dates('2025-01-01','2026-09-30',n_dirty)]
raw_cities = choice(['Delhi','delhi','DELHI','Mumbai','mumbai','Bengaluru','Bangalore','Chennai','chennai','Kathua','KATHUA',' Jaipur ','Pune','Kolkata'],n_dirty).astype(object)
raw_sales = np.round(np.exp(rng.normal(7.0,1.0,n_dirty)),2).astype(object)
for i in rng.choice(np.arange(n_dirty),size=18,replace=False): raw_sales[i]=choice(['unknown','N/A','', '₹1,250'])
for i in rng.choice(np.arange(n_dirty),size=8,replace=False): raw_sales[i]=-abs(float(rng.integers(50,1200)))
for i in rng.choice(np.arange(n_dirty),size=5,replace=False): raw_sales[i]=round(float(rng.integers(100000,500000)),2)
for i in rng.choice(np.arange(n_dirty),size=10,replace=False): raw_dates[i]=choice(['not available','2025/13/40','', '31-02-2025'])
raw_quantity=rng.integers(1,10,n_dirty).astype(object)
for i in rng.choice(np.arange(n_dirty),size=7,replace=False): raw_quantity[i]=choice(['two','', '3 units'])
dirty=pd.DataFrame({'record_id':[f'D{i:05d}' for i in range(1,n_dirty+1)],'order_date_raw':raw_dates,'city_raw':raw_cities,'product_category_raw':choice(['Electronics','electronics','ELECTRONICS','Home','Home ','Grocery','Fashion','Books','Beauty'],n_dirty),'quantity_raw':raw_quantity,'sales_raw':raw_sales,'coupon_code_raw':[choice(['SAVE10','WELCOME','FESTIVE',None,' none ','']) for _ in range(n_dirty)],'customer_email_raw':[f'user{int(x)}@example.test' if rng.random()>.07 else None for x in rng.integers(1,600,n_dirty)]})
# Add exact duplicate rows to make drop_duplicates practice obvious.
dirty=pd.concat([dirty,dirty.iloc[[7,25,49,88,120]]],ignore_index=True)
write(dirty,'messy_sales.csv')

# ---------- data dictionary / guide ----------
description = {
'customers.csv':'One row per fictional customer. Profile, acquisition, loyalty and satisfaction fields; optional values are intentional.',
'products.csv':'One row per fictional product. Categories, prices, costs, weights, stock targets and ratings.',
'orders.csv':'One row per order. Customer foreign key, order lifecycle timestamps, status, channel, shipping, tax and total amounts.',
'order_items.csv':'One row per product line within an order. Join to orders by order_id and products by product_id.',
'retail_transactions.csv':'Convenience flat table: order items joined to order, product and customer attributes. Best starting point if you want one file.',
'website_events.csv':'One row per online event with timestamps, sessions, channel, event type, device, duration and conversion fields.',
'daily_regional_metrics.csv':'Daily website and sales metrics by region over several years. A small fraction of dates is omitted intentionally for time-series resampling/reindexing practice.',
'inventory_movements.csv':'Stock movements by product, warehouse, type, date and signed quantity change.',
'employees.csv':'Fictional workforce data for grouping, aggregation, dates, sorting, ranking and statistical analysis.',
'survey_responses.csv':'Customer feedback with rating scales, dates, categories, optional customer IDs and free-text comments.',
'messy_sales.csv':'Intentionally untidy practice data: duplicates, inconsistent capitalization/spacing, missing entries, invalid dates, non-numeric strings, negative values and outliers.'}
field_notes = {
'customer_id':'Customer identifier; links customers to orders and optional feedback/events.', 'product_id':'Product identifier; links products to order items and inventory.',
'order_id':'Order identifier; links order headers to their item lines.', 'order_date':'Timestamp/date associated with an order.',
'net_sales':'Item revenue after line discount, before order-level shipping and tax.', 'order_total':'Item net sales plus shipping fee and tax amount.',
'quantity_change':'Signed inventory movement: positive adds stock, negative reduces stock.',
'conversion_rate':'Orders divided by visits for a daily region record.', 'event_timestamp':'When the web event occurred; useful for .dt, sorting, resampling and time windows.',
'customer_rating':'Product rating on a one-to-five scale; missing ratings are intentional.',
}
dict_rows=[]
for fn, desc in description.items():
    df=pd.read_csv(DATA/fn, nrows=10)
    for col in df.columns:
        sample = next((str(x) for x in df[col].dropna().head(3).tolist()), '')
        dict_rows.append({'file':fn,'column':col,'pandas_dtype_example':str(df[col].dtype),'description': desc if col==df.columns[0] else field_notes.get(col,''),'example_non_null_value':sample})
pd.DataFrame(dict_rows).to_csv(ROOT/'data_dictionary.csv',index=False)

readme = '''# Python Data Analysis Playground

A reusable, synthetic data collection designed for practising Python's NumPy and pandas libraries without continually searching for new datasets.

## Start here

**Open `data/retail_transactions.csv` first.** It is a wide, ready-to-analyse table combining order items with order, product and customer attributes. It is the easiest file for your first experiments with filtering, arithmetic, NumPy arrays, sorting, grouping, aggregation, missing values, strings and charts.

When you are ready for real relational-data practice, use `customers.csv`, `products.csv`, `orders.csv` and `order_items.csv` separately and join them with `merge()`.

All records are synthetic and fictional. They do not describe real customers, staff, or transactions. The random seed is fixed in `generate_dataset.py`, so you can regenerate the same data.

## Files at a glance

| File | Main practice opportunities |
|---|---|
| `retail_transactions.csv` | Single-table analysis; arithmetic, masks, groupby, aggregation, sorting, ranking, correlations, plotting |
| `customers.csv` | Strings, categories, missing values, filtering, `value_counts`, mapping, customer segmentation |
| `products.csv` | Numeric summaries, categories, sorting, `where`, `select`, arrays, price/cost calculations |
| `orders.csv` | Dates, time differences, statuses, conditional columns, date parts, groupby and order-level summaries |
| `order_items.csv` | Line-level totals, multiple rows per order, duplicates checks, joins and reshaping |
| `website_events.csv` | High-volume event data, datetimes, sessions, event frequencies, conversion analysis |
| `daily_regional_metrics.csv` | Time series, missing dates, `resample`, rolling windows, shifts, cumulative calculations, trends |
| `inventory_movements.csv` | Positive/negative values, stock changes, grouping and cumulative totals |
| `employees.csv` | Department summaries, salary distributions, ranking, quantiles, correlations and date calculations |
| `survey_responses.csv` | Ordinal ratings, text methods, missing data, NPS-style summaries and categories |
| `messy_sales.csv` | Deliberately dirty data for `isna`, `dropna`, `fillna`, `duplicated`, `drop_duplicates`, `to_numeric`, `to_datetime`, `str` methods and outlier detection |
| `data_dictionary.csv` | Column names, example data types, sample values and brief descriptions |

## Loading the files

```python
import numpy as np
import pandas as pd
from pathlib import Path

DATA = Path("data")  # Run your notebook from this project folder
transactions = pd.read_csv(DATA / "retail_transactions.csv", parse_dates=["order_date", "ship_date", "delivery_date", "signup_date"])
customers = pd.read_csv(DATA / "customers.csv", parse_dates=["signup_date"])
products = pd.read_csv(DATA / "products.csv", parse_dates=["launch_date"])
orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date", "ship_date", "delivery_date", "promised_delivery_date"])
items = pd.read_csv(DATA / "order_items.csv")
daily = pd.read_csv(DATA / "daily_regional_metrics.csv", parse_dates=["date"])
events = pd.read_csv(DATA / "website_events.csv", parse_dates=["event_timestamp"])
```

If a relative path does not work, print `Path.cwd()` to see your current working directory, or use the full path to the `data` folder. In VS Code, place your notebook or `.py` file in this project folder.

## Important data notes

- IDs such as `C00001` and `P0001` are text identifiers, not numbers to calculate with.
- In `retail_transactions.csv`, a single order may appear on multiple rows because each row represents one line item. Do not sum `order_total` across this table unless you first reduce to one row per order; otherwise the order total will be repeated once for every item.
- `net_sales` is line-item sales after its line discount. `order_total` includes item sales, shipping and tax. The fields are intentionally distinct.
- The primary business tables are mostly structured and suitable for analytical practice. `messy_sales.csv` is intentionally untidy. Some tables also contain a modest amount of missing optional data.
- A small proportion of daily dates are missing in `daily_regional_metrics.csv` so you can practise reindexing and resampling.
- A few domain details are simulated for learning and should not be treated as real business facts.

## NumPy and pandas practice map

The accompanying `PRACTICE_ROADMAP.md` maps a broad range of commonly used NumPy and pandas operations to these tables. No finite dataset can meaningfully exercise literally every function in either library—specialized functions exist for image arrays, linear algebra, sparse matrices, geospatial data, and more—but this collection covers a broad range of practical data-analysis workflows.
'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')

roadmap='''# NumPy + pandas practice roadmap

Work through these sections in order. Try each task yourself before looking up syntax. Use `retail_transactions.csv` as the default dataset unless another file is named.

## 1. Loading, inspecting and understanding data
**Files:** all tables

- `pd.read_csv()`, `head()`, `tail()`, `sample()`, `shape`, `columns`, `index`, `dtypes`, `info()`, `describe()`, `memory_usage()`.
- `value_counts()`, `nunique()`, `unique()`, `select_dtypes()`, `is_numeric_dtype()`.
- Questions: How many rows and columns are in each table? Which columns are numeric, categorical, dates or identifiers? Which columns have missing values?

## 2. Selecting rows and columns
**File:** `retail_transactions.csv`, `customers.csv`

- Column selection, lists of columns, `.loc`, `.iloc`, boolean masks, `isin()`, `between()`, `query()`, `at`, `iat`, `where()`, `mask()`.
- Questions: Find delivered orders from one city; select products within a price range; find customers whose satisfaction score is missing.

## 3. NumPy foundations and vectorized calculations
**Files:** `products.csv`, `retail_transactions.csv`

- `np.array`, `shape`, `ndim`, `dtype`, `astype`, `arange`, `linspace`, `zeros`, `ones`, `full`, `eye`, `reshape`, `ravel`, `flatten`, `transpose`, `squeeze`, `concatenate`, `stack`, `vstack`, `hstack`, `split`.
- Math: `sum`, `mean`, `median`, `std`, `var`, `min`, `max`, `ptp`, `percentile`, `quantile`, `round`, `floor`, `ceil`, `sqrt`, `log`, `exp`, `clip`, `isfinite`, `isnan`.
- Logic and selection: comparisons, boolean masks, `where`, `select`, `all`, `any`, `nonzero`, `argmin`, `argmax`, `argsort`, `sort`, `unique`, `bincount`, `count_nonzero`.
- Randomness and sampling: `default_rng`, `integers`, `choice`, `normal`, `uniform`, `permutation`, `shuffle`, `seed` concepts.
- Broadcasting: calculate margins or discount amounts for arrays of many products; explain the shapes before doing the calculation.
- Questions: Which products have the highest gross margin? What is the 90th percentile order-line value? Flag values above a threshold using `np.where()`.

## 4. Arithmetic, derived columns and functions
**File:** `retail_transactions.csv`

- Vectorized operators, `.add()`, `.sub()`, `.mul()`, `.div()`, `.round()`, `.clip()`, `.abs()`, `.pow()`, `.eval()`, `.assign()`, `apply()`, `map()`, `replace()`, `pipe()`.
- Questions: Calculate margin amount and margin percentage, classify order lines, compute a discount band, create a high-value flag.

## 5. Sorting, ranking and top-N analysis
**Files:** `products.csv`, `employees.csv`, `retail_transactions.csv`

- `sort_values()`, `sort_index()`, `nlargest()`, `nsmallest()`, `rank()`, `idxmax()`, `idxmin()`, `duplicated()`.
- Questions: Find the 10 most expensive products; rank employees by salary within a department; identify the customers with the most purchase lines.

## 6. Missing data and data quality
**Files:** `messy_sales.csv`, `customers.csv`, `survey_responses.csv`

- `isna()`, `notna()`, `dropna()`, `fillna()`, `ffill()`, `bfill()`, `interpolate()`, `drop_duplicates()`, `duplicated()`, `replace()`, `astype()`, `convert_dtypes()`, `pd.to_numeric(errors="coerce")`, `pd.to_datetime(errors="coerce")`.
- Questions: Standardize city names; convert sales strings to numbers; identify invalid dates; decide which missing values should be dropped, filled or left missing. Explain why each choice is defensible.

## 7. String operations and text cleaning
**Files:** `customers.csv`, `messy_sales.csv`, `survey_responses.csv`

- `.str.lower()`, `.str.upper()`, `.str.title()`, `.str.strip()`, `.str.contains()`, `.str.startswith()`, `.str.endswith()`, `.str.replace()`, `.str.split()`, `.str.extract()`, `.str.len()`, `.str.pad()`, `.str.match()`.
- Questions: normalize city and category labels; identify comments mentioning delivery; extract the email domain; clean inconsistent coupon values.

## 8. Dates and times
**Files:** `orders.csv`, `website_events.csv`, `daily_regional_metrics.csv`

- `pd.to_datetime()`, `.dt.year`, `.dt.month`, `.dt.day`, `.dt.day_name()`, `.dt.dayofweek`, `.dt.quarter`, `.dt.is_month_end`, `.dt.days_in_month`, date subtraction, `Timedelta`, `DateOffset`, `Period`, `PeriodIndex`, `DateTimeIndex`, `resample()`.
- Questions: Calculate delivery duration; compare weekday and weekend sales; aggregate to month and quarter; find the busiest hour of day in website events.

## 9. Grouping and aggregation
**Files:** `retail_transactions.csv`, `employees.csv`, `inventory_movements.csv`

- `groupby()`, `agg()`, `transform()`, `filter()`, `size()`, `count()`, `sum()`, `mean()`, `median()`, `min()`, `max()`, `std()`, `nunique()`, named aggregation, multiple grouping keys.
- Questions: revenue by category; average salary by department; inventory change by product and warehouse; normalize each employee's salary against their own department's average with `transform()`.

## 10. Combining data: joins and concatenation
**Files:** customers, orders, order_items, products, inventory

- `merge()` with `inner`, `left`, `right`, and `outer`; `validate`; `indicator`; `suffixes`; `join()`; `concat()` along rows and columns; `keys`; index alignment.
- Questions: attach customer attributes to orders; find customers with no orders; check whether every order item references a valid product; combine monthly extracts.

## 11. Reshaping tables
**Files:** `retail_transactions.csv`, `daily_regional_metrics.csv`

- `pivot()`, `pivot_table()`, `melt()`, `stack()`, `unstack()`, `wide_to_long()`, `crosstab()`, `explode()`, `get_dummies()`, `factorize()`.
- Questions: make a region-by-month revenue grid; compare average product sales by city; reshape a wide summary into tidy long format; produce a category-by-channel count table.

## 12. Time-series analysis
**File:** `daily_regional_metrics.csv`

- Set a datetime index, `resample()`, `asfreq()`, `reindex()`, `rolling()`, `expanding()`, `ewm()`, `shift()`, `diff()`, `pct_change()`, `cumsum()`, `cumprod()`, `cummin()`, `cummax()`, `to_period()`.
- Questions: calculate a 7-day moving average; compare daily revenue with the previous week; calculate monthly region totals and cumulative revenue; restore missing calendar dates before filling them thoughtfully.

## 13. Statistics and relationships
**Files:** `retail_transactions.csv`, `employees.csv`, `daily_regional_metrics.csv`

- `corr()`, `cov()`, `quantile()`, `value_counts(normalize=True)`, `describe()`, `corrwith()`, `mode()`, `sem()`, `skew()`, `kurt()`, `cut()`, `qcut()`.
- Questions: study how discount relates to quantity; compare salary distributions by department; create quartile groups for order values. Remember correlation does not establish causation.

## 14. Indexing and alignment concepts
**Any DataFrame**, especially `customers.csv` and `orders.csv`

- `set_index()`, `reset_index()`, `reindex()`, `rename_axis()`, `rename()`, `droplevel()`, `swaplevel()`, `sort_index()`, `.align()`, `combine_first()`, MultiIndex grouping and selection.
- Questions: index orders by ID; create a customer-month MultiIndex summary; inspect how pandas aligns rows when adding two Series with different indexes.

## 15. Categories, encoding and frequency analysis
**Files:** `customers.csv`, `products.csv`, `website_events.csv`, `survey_responses.csv`

- `astype("category")`, `.cat.categories`, `.cat.codes`, `.cat.set_categories()`, `get_dummies()`, `factorize()`, `crosstab()`, `value_counts()`.
- Questions: order loyalty tiers logically; encode category variables; compare traffic sources across devices.

## 16. Files, exports and reproducible workflows
**All tables**

- `to_csv()`, `read_csv()` options such as `usecols`, `dtype`, `parse_dates`, `na_values`, `chunksize`; `to_json()`, `read_json()`, `to_excel()`/`read_excel()` where Excel support is installed; pickle only for trusted local workflows.
- Questions: save a cleaned table; export a pivot to CSV; read only selected columns; process the larger events table in chunks.

## 17. Integrated mini-projects

1. **Retail performance:** category and city revenue, average order value, discounts, and return patterns. Avoid double-counting order-level totals in the line-level flat table.
2. **Customer behaviour:** acquisition channel, loyalty tier, repeat purchase frequency and satisfaction.
3. **Website funnel:** event counts through product views, cart, checkout and purchase by device and traffic source.
4. **Inventory control:** cumulative stock change by product/warehouse, damaged goods and frequent adjustments.
5. **People analytics:** department salary comparisons, tenure and performance relationships. Treat simulated results as practice only.
6. **Dirty data rescue:** take `messy_sales.csv` from raw input to a documented, validated clean table.
7. **Time-series report:** daily to weekly/monthly resampling, rolling averages, missing dates and region comparisons.

## A useful habit

For every function you practise, write four things: (1) what problem it solves, (2) what input shape it expects, (3) what output it returns, and (4) one small example from this dataset. This builds understanding rather than memorizing function names.
'''
(ROOT/'PRACTICE_ROADMAP.md').write_text(roadmap,encoding='utf-8')

# ---------- starter notebook ----------
try:
    import nbformat as nbf
    nb=nbf.v4.new_notebook()
    nb['metadata']={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.x'}}
    cells=[]
    cells.append(nbf.v4.new_markdown_cell('# Python Data Analysis Playground\n\nStart with the wide retail table, then load individual tables as needed. All data is synthetic.'))
    cells.append(nbf.v4.new_code_cell('from pathlib import Path\nimport numpy as np\nimport pandas as pd\n\nDATA = Path("data")\ntransactions = pd.read_csv(DATA / "retail_transactions.csv", parse_dates=["order_date", "ship_date", "delivery_date", "signup_date"])\ncustomers = pd.read_csv(DATA / "customers.csv", parse_dates=["signup_date"])\nproducts = pd.read_csv(DATA / "products.csv", parse_dates=["launch_date"])\norders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date", "ship_date", "delivery_date", "promised_delivery_date"])\nitems = pd.read_csv(DATA / "order_items.csv")\ndaily = pd.read_csv(DATA / "daily_regional_metrics.csv", parse_dates=["date"])\nevents = pd.read_csv(DATA / "website_events.csv", parse_dates=["event_timestamp"])\n\nprint("Transactions shape:", transactions.shape)\ntransactions.head()'))
    cells.append(nbf.v4.new_markdown_cell('## First exploration\nRun each cell, then try changing the columns or conditions.'))
    cells.append(nbf.v4.new_code_cell('transactions.info()\ntransactions.describe(include="all").T'))
    cells.append(nbf.v4.new_code_cell('transactions.isna().sum().sort_values(ascending=False).head(15)'))
    cells.append(nbf.v4.new_markdown_cell('## NumPy practice: vectorized calculations\nCreate arrays from columns and calculate a simple margin.'))
    cells.append(nbf.v4.new_code_cell('prices = products["list_price"].to_numpy()\ncosts = products["unit_cost"].to_numpy()\nmargin = prices - costs\nmargin_pct = np.divide(margin, prices, out=np.zeros_like(margin, dtype=float), where=prices != 0)\nprint("Median margin:", np.median(margin).round(2))\nprint("90th percentile list price:", np.quantile(prices, 0.90).round(2))\nprint("Highest-margin product row index:", np.argmax(margin))'))
    cells.append(nbf.v4.new_markdown_cell('## pandas practice: filtering, grouping and sorting'))
    cells.append(nbf.v4.new_code_cell('high_value = transactions.loc[transactions["net_sales"] >= 5000, ["order_id", "product_name", "category", "quantity", "net_sales"]]\nhigh_value.head(10)'))
    cells.append(nbf.v4.new_code_cell('transactions.groupby("category", dropna=False).agg(\n    line_count=("order_item_id", "count"),\n    units_sold=("quantity", "sum"),\n    net_sales=("net_sales", "sum"),\n    average_line_sales=("net_sales", "mean")\n).sort_values("net_sales", ascending=False)'))
    cells.append(nbf.v4.new_markdown_cell('## Joins: understand relational data'))
    cells.append(nbf.v4.new_code_cell('orders_with_customer = orders.merge(customers, on="customer_id", how="left", validate="many_to_one", indicator=True)\norders_with_customer["_merge"].value_counts()'))
    cells.append(nbf.v4.new_markdown_cell('## Time series: rolling average'))
    cells.append(nbf.v4.new_code_cell('north = (daily.loc[daily["region"] == "North"]\n         .sort_values("date")\n         .set_index("date"))\nnorth["revenue_7_day_average"] = north["revenue"].rolling("7D").mean()\nnorth[["revenue", "revenue_7_day_average"]].head(12)'))
    cells.append(nbf.v4.new_markdown_cell('## Cleaning challenge\nUse `messy_sales.csv` to standardize city labels, parse dates, convert sales to numeric values, identify duplicates and negative/outlier values. Record your cleaning decisions before removing any row.'))
    cells.append(nbf.v4.new_code_cell('messy = pd.read_csv(DATA / "messy_sales.csv")\nprint("Shape:", messy.shape)\nprint("Duplicate rows:", messy.duplicated().sum())\nmessy.head(10)'))
    cells.append(nbf.v4.new_markdown_cell('For many more tasks, open `PRACTICE_ROADMAP.md`. It is a broad reference map from NumPy/pandas concepts to relevant files and exercises.'))
    nb['cells']=cells
    nbf.write(nb, ROOT/'00_start_here.ipynb')
except Exception as e:
    (ROOT/'NOTEBOOK_BUILD_NOTE.txt').write_text(f'Notebook generation skipped: {e}\n',encoding='utf-8')

# A compact machine-readable manifest helps users inspect files programmatically.
manifest=[]
for p in sorted(DATA.glob('*.csv')):
    df=pd.read_csv(p)
    manifest.append({'file':p.name,'rows':len(df),'columns':len(df.columns),'size_kb':round(p.stat().st_size/1024,1)})
(ROOT/'dataset_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

# Zip the whole project folder for convenient download.
zip_path=ROOT.parent/'python_data_analysis_playground.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as zf:
    for p in ROOT.rglob('*'):
        if p.is_file():
            zf.write(p, p.relative_to(ROOT.parent))
print('Created project:', ROOT)
print('Zip:', zip_path)
print(pd.DataFrame(manifest).to_string(index=False))
