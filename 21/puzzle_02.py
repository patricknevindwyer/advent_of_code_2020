import sys


def read_ingredients(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    
    # store one entry of two sets per line item
    entries = []
    for line in raw.split("\n"):
        line = line.strip()
        ings_r, allers_r = line.split(" (")
        ings = set(ings_r.strip().split(" "))
        allers = set(allers_r.strip(")").replace("contains ", "").split(", "))
        entries.append(
            {
                "ingredients": ings,
                "allergens": allers,
                "full_ingredients": ings_r.strip().split(" ")
            }
        )
    
    return entries


def remove_allergens(foods):
    
    # track dangerous ingredient lists
    dangerous_ingredients = []
    
    # find all allergens
    allergens = []
    for food in foods:
        allergens += food["allergens"]
    allergens = list(set(allergens))
    
    print("Filtering for %d allergens" % (len(allergens),))
    print(allergens)
    
    # one by one we eliminate by entry
    while len(allergens) > 0:
        removal_ingredient = []
        removal_allergen = []
        
        # search through every allergen and try to remove it
        for allergen in allergens:
            foods_with_allergen = [f["ingredients"] for f in foods if allergen in f["allergens"]]
        
            print("Allergen: %s" % (allergen,))
            print("   Foods: ", foods_with_allergen)
        
            # can we remove by unique set? intersection
            intersection = full_intersection(foods_with_allergen)
            if len(intersection) == 1:
                print("    ! intersectional match: %s" % (list(intersection)[0],))
                removal_ingredient.append(list(intersection)[0])
                removal_allergen.append(allergen)
                continue
            
            # can we remove by single elimination?
            if len(foods_with_allergen) == 1:
                if len(foods_with_allergen[0]) == 1:
                    print("    ! single ingredient elimination: %s" % (list(foods_with_allergen[0])[0],))
                    removal_ingredient.append(list(foods_with_allergen[0])[0])
                    removal_allergen.append(allergen)
        
        # quick track our dangerous ingredients
        for idx in range(len(removal_allergen)):
            dangerous_ingredients.append( (removal_allergen[idx], removal_ingredient[idx]) )
            
        # now remove anything we've matched/reduced from the allergen and ingredient
        # lists, so we can continue
        for rem_ing in removal_ingredient:
            for food in foods:
                if rem_ing in food["ingredients"]:
                    food["ingredients"].remove(rem_ing)
    
        for rem_all in removal_allergen:
            allergens.remove(rem_all)
            for food in foods:
                if rem_all in food["allergens"]:
                    food["allergens"].remove(rem_all)
    
    return dangerous_ingredients, foods
    

def full_intersection(ingredient_list):
    
    a = ingredient_list[0]
    
    for b in ingredient_list[1:]:
        a = a.intersection(b)
    
    return a


def allergy_list(dangers):
    return ",".join([d[1] for d in sorted(dangers, key=lambda d: d[0])])
    
    
if __name__ == "__main__":
    foods = read_ingredients(sys.argv[-1])
    danger, safe_foods = remove_allergens(foods)
    print(danger)
    print(allergy_list(danger))