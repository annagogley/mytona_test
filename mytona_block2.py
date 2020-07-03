import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('/Users/annagogley/Downloads/data.csv')

#узнаем неуникальные значения
print(data.nunique())
fig = plt.figure()
plt.bar(data['Date'], data['Count'])
plt.title('Дата и количество покупок')
plt.grid(True)
plt.show()

#узнали с какой по какую строку длится период 10/18/2017 и 10/19/2017: 3784:4199
for i in range(len(data.Date)):
    if data.Date[i] == '10/20/2017':
        print(i)
        break

#из каких магазинов было большинство покупок 10/18/2017 и 10/19/2017
total_count = data.loc[3784:4199,['From', 'Count']]
print("% Sale1 to total count within 2 days:",
      sum(total_count.loc[total_count.From == 'Sale1', 'Count'])/sum(total_count['Count']))
print("% Sale2 to total count within 2 days:",
      sum(total_count.loc[total_count.From == 'Sale2', 'Count'])/sum(total_count['Count']))
print("% Store1 to total count within 2 days:",
      sum(total_count.loc[total_count.From == 'Store1', 'Count'])/sum(total_count['Count']))
print("% Store2 to total count within 2 days:",
      sum(total_count.loc[total_count.From == 'Store2', 'Count'])/sum(total_count['Count']))

#количество покупок в магазинах после 10/19/2017
total_count2 = data.loc[4200:,['From','Count']]
print("% Sale1 to total count after the sale:",
      sum(total_count2.loc[total_count2.From == 'Sale1', 'Count'])/sum(total_count2['Count']))
print("% Sale2 to total count after the sale:",
      sum(total_count2.loc[total_count2.From == 'Sale2', 'Count'])/sum(total_count2['Count']))
print("% Store1 to total count after the sale:",
      sum(total_count2.loc[total_count2.From == 'Store1', 'Count'])/sum(total_count2['Count']))
print("% Store2 to total count after the sale:",
      sum(total_count2.loc[total_count2.From == 'Store2', 'Count'])/sum(total_count2['Count']))

#количество покупок в магазинах до 10/18/2017
total_count2 = data.loc[:3784,['From','Count']]
print("% Sale1 to total count before the sale:",
      sum(total_count2.loc[total_count2.From == 'Sale1', 'Count'])/sum(total_count2['Count']))
print("% Sale2 to total count before the sale:",
      sum(total_count2.loc[total_count2.From == 'Sale2', 'Count'])/sum(total_count2['Count']))
print("% Store1 to total count before the sale:",
      sum(total_count2.loc[total_count2.From == 'Store1', 'Count'])/sum(total_count2['Count']))
print("% Store2 to total count before the sale:",
      sum(total_count2.loc[total_count2.From == 'Store2', 'Count'])/sum(total_count2['Count']))


#сколько процентов от общих покупок заняли покупки вип пользователей
vip_count = data.loc[data.VIP == 1]['Count']
rate_VIP = sum(vip_count)/sum(data.Count)
print("% users that bought items who has VIP status:", rate_VIP)

#самый часто покупаемый предмет
energy = 0
bonus = 0
collections = 0
for i in range(len(data.item_id)):
    if data.item_id[i] // 10000 == 1:
        energy += data.Count[i]
    elif data.item_id[i] // 10000 == 2:
        bonus += data.Count[i]
    else:
        collections += data.Count[i]
print("Всего куплено предметов: \n %d энергии \n %d бонусов \n %d коллекционных предметов"
      % (energy, bonus, collections))

#посмотрим какого качества предметы покупают и сколько
#записываем в лист качество предметов


def item_qual(t, column):
    qual = []
    for i in range(len(column)):
        if column[i] // 10000 == t:
            qual.append(column[i] % 10000)
    return qual


bonus_qual = item_qual(2, data.item_id)
energy_qual = item_qual(1, data.item_id)
c_qual = item_qual(3, data.item_id)

#составляем словарь с качеством предмета и количеством


def store_count(list, set_of_list, dict):
    for value in set_of_list:
        dict.update({value:0})
    for i in list:
        local_value = dict[i] + 1
        dict.update({i: local_value})
    return dict
b_dict = {}
set_of_list = set(bonus_qual)
e_dict = {}
set_of_list_e = set(energy_qual)
c_dict = {}
set_of_list_c = set(c_qual)
print("качество купленных бонусов: \n", store_count(bonus_qual,set_of_list,b_dict))
print("качество купленной энергии: \n", store_count(energy_qual,set_of_list_e,e_dict))
print("качество купленных коллекций: \n", store_count(c_qual,set_of_list_c,c_dict))

#какие предметы где покупаются
e_store = []
b_store = []
c_store = []
for i in range(len(data.item_id)):
    if data.item_id[i] // 10000 == 1:
        e_store.append(data.From[i])
    elif data.item_id[i] // 10000 == 2:
        b_store.append(data.From[i])
    else:
        c_store.append(data.From[i])

e_st = {}
b_st = {}
c_st = {}
set_e_st = set(e_store)
set_b_st = set(b_store)
set_c_st = set(c_store)
print("покупки энергии в магазинах: \n", store_count(e_store, set_e_st, e_st))
print("покупки бонусов в магазинах: \n", store_count(b_store, set_b_st, b_st))
print("покупки коллекций в магазинах: \n", store_count(c_store, set_c_st, c_st))

#узнаем какие предметы покупают чаще всего на каждом уровне
levels = set(data.Level)
l_dict = store_count(data.Level, levels, {})
print("количество игроков на каждом уровне: \n",l_dict)

result_dict = {}
for level in levels:
    result_dict.update({level: []})

for row in range(len(data)):
    level_data = {}
    clearly_item_id = data.item_id[row] // 10000
    level_data.update({clearly_item_id: data.Count[row]})
    if result_dict[data.Level[row]]:
        level_stored = False
        for item_data in result_dict[data.Level[row]]:
            if clearly_item_id in item_data.keys():
                item_data[clearly_item_id] += data.Count[row]
                level_stored = True
        if not level_stored:
            result_dict[data.Level[row]].append(level_data)
    else:
        result_dict.update({data.Level[row]: [level_data]})

print("В каких предметах больше всего потребности у игроков на каждом уровне? \n",result_dict)

vip_levels = {}
for value in levels:
    vip_levels.update({value:0})
for j in range(len(data.VIP)):
    if data.VIP[j] == 1 and data.Level[j] in vip_levels:
        local_value = vip_levels[data.Level[j]] + 1
        vip_levels.update({data.Level[j]: local_value})
print("Сколько випов на каждом уровне: \n",vip_levels)