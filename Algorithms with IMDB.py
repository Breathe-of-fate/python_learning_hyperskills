def merge_sort_movies(movies):
    if len(movies) > 1:
        mid = len(movies) // 2
        left_half = movies[:mid]
        right_half = movies[mid:]
        merge_sort_movies(left_half)
        merge_sort_movies(right_half)
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i][1] < right_half[j][1]:
                movies[k] = left_half[i]
                i += 1
            else:
                movies[k] = right_half[j]
                j += 1
            k += 1
        while i < len(left_half):
            movies[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            movies[k] = right_half[j]
            j += 1
            k += 1
    return movies

def binary(data):
    left = 0
    right = len(data)-1
    mid = (left+right) // 2
    while left <= right:
        if data[mid][1] == 6.0:
            lower_bound = mid-1
            upper_bound = mid+1
            while data[lower_bound-1][1] == 6.0:
                lower_bound=lower_bound-1
            while data[upper_bound+1][1] == 6.0:
                upper_bound=upper_bound+1
            for index in range(lower_bound,upper_bound+1):
                print(f"{data[index][0]} - {data[index][1]}")
            return
        elif data[mid][1] < 6.0:
            left = mid+1
        else:
            right = mid-1
        mid = (left + right) // 2

data = []

with open("movies.csv", "r", encoding="utf-8") as file:
    for line in file:
        title, rating = line.rstrip().rsplit(',', 1)
        data.append((title.strip('"'), float(rating)))

sorted_movies = merge_sort_movies(data)
binary(sorted_movies)