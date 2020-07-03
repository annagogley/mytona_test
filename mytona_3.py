import pandas as pd

#загружаем данные
data = pd.read_csv("/Users/annagogley/Downloads/block3.csv")
item = pd.read_csv("/Users/annagogley/Downloads/block3_item.csv")

total_skill = 100
player_level = [1]
ye = []
ye2 = 0
ye4 = 0

#основной цикл по дням
for i in range(1,len(data.Day)):
    total_skill += data.Daily_skill[i]
    #увеличение уровня при достижении суммы очков в 300 или если конец недели
    if total_skill%300 == 0 or data.Daily_skill[i]>100:
        player_level.append(1+ total_skill//300)
    #иначе добавляем в массив предыдущий результат
    else:
        player_level.append(player_level[i-1])
    #сравниваем есть ли текущий уровень в списке с фруктами, прибавляем условные единицы
    if ((player_level[i] in set(item.Level)) and (player_level[i] != player_level[i-1])):
        item_ye = list(item.loc[item.Level == (player_level[i]), 'item_ye'])[0]
        ye.append(item_ye)
        ye2 += item_ye
    #если скачок уровня произошел больше, чем на 1 (выходные), то будем проверять наличие фруктов в промежуточных уровнях
    elif player_level[i] - player_level[i-1] > 1:
        for j in range(1, player_level[i] - player_level[i-1]):
            if (player_level[i-1]+j) in list(item.Level):
                item_ye2 = list(item.loc[item.Level == (player_level[i-1]+j), 'item_ye'])[0]
                ye.append(item_ye2)
                ye2 += item_ye2
    
    pokupka = 120
    level_count = 5
    #покупаем уровни по 5 штук при первой возможности
    while ye2 > pokupka:
        total_skill += (ye2 // pokupka) * level_count*300
        level_now = player_level[i]
        player_level.insert(i, level_now+(ye2 // pokupka) * level_count)
        player_level.pop()
        ye3 = ye2
        ye2 = ye2 % pokupka
        for k in range(1, player_level[i] - player_level[i - 1] + (ye3 // pokupka) * level_count):
            if ye3 // pokupka >= 1:
                abe = (player_level[i-1]+k+(ye3 // pokupka) * level_count)
                if abe in list(item.Level):
                    item_ye2 = list(item.loc[item.Level == (player_level[i-1]+k + (ye3 // pokupka) * level_count), 'item_ye'])[0]
                    ye.append(item_ye2)
                    ye2 += item_ye2
                    ye4 += ye3
                    ye3 = ye3 % pokupka


print("Остаток: ", ye2, "Всего заработано:", ye4)
print("Всего очков: ", total_skill, "Уровень: ", player_level[49])
#подсчет количества фруктов
ye_set = set(ye)
ye_dict = {}
for val in ye_set:
    ye_dict.update({val: 0})
for val in ye:
    local_val = ye_dict[val] + 1
    ye_dict.update({val: local_val})
print(ye_dict)
