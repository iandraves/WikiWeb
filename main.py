import wikipedia
import concurrent.futures

not_done = True

def main():
	# Searching for first page
	try:
		first_page = input("First Page Title: ")
		first_page_title = wikipedia.search(first_page, results=1, suggestion=False)[0]
		print("--> Found: '" + first_page_title + "'")
	except:
		print("Invalid search query! Try again.")
		main()

	# Searching for second page
	try:
		second_page = input("Second Page Title: ")
		second_page_title = wikipedia.search(second_page, results=1, suggestion=False)[0]
		print("--> Found: '" + second_page_title + "'")
	except:
		print("Invalid search query! Try again.")
		main()

	# Loading pages
	print("Loading page data...")
	first_page_wikis = wikipedia.page(title=first_page_title, pageid=None, auto_suggest=False, redirect=True, preload=False).links
	second_page_wikis = wikipedia.page(title=second_page_title, pageid=None, auto_suggest=False, redirect=True, preload=False).links

	# Running concurrent searches
	print("Crawling wikis...")
	futures = []
	with concurrent.futures.ThreadPoolExecutor() as executor:
		first_search_path = executor.submit(search, first_page_title, second_page_title, first_page_wikis, 1)
		second_search_path = executor.submit(search, second_page_title, first_page_title, second_page_wikis, 1)

		futures.append(first_search_path)
		futures.append(second_search_path)

		# Waiting for match and outputting result
		for future in concurrent.futures.as_completed(futures):
			global not_done
			not_done = False
			if future.result() != None:
				if future.result() == 1:
					print("There is 1 degree of separation between '" + first_page_title + "' and " + "'" + second_page_title + "'")
				else:
					print("There are " + str(future.result()) + " degrees of separation between '" + first_page_title + "' and " + "'" + second_page_title + "'")
		
def search(start_page_title, end_page_title, wikis, degrees):
	while not_done:
		# Checking current degree for match
		if end_page_title in wikis:
			return degrees
		else:
			degrees += 1

		# Checking next degree & creating subsequent one
		new_wikis = []
		for wiki_page in wikis:
			if not not_done:
				return None
			else:
				print("Checking '" + wiki_page + "' on degree level " + str(degrees), "(" + start_page_title + " --> " + end_page_title + ")")

				try:
					sub_wikis = wikipedia.page(title=wiki_page, pageid=None, auto_suggest=True, redirect=True, preload=False).links
					
					if end_page_title in sub_wikis:
						return degrees
					
					new_wikis.extend(sub_wikis)
				except:
					continue
		
		# Removing duplicates
		new_wikis = list(dict.fromkeys(new_wikis))

		# Searching new list
		search(start_page_title, end_page_title, new_wikis, degrees)
	
	return None

if __name__ == '__main__':
	main()