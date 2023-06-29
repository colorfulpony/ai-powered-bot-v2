link1 = "alleycorp.com/companies/"
link2 = "https://alleycorp.com/companies/mongodb/"

# Extract the domain and path from link1
domain1, path1 = link1.split('/', 1)

# Extract the domain and path from link2
url_parts = link2.split('/', 3)
domain2 = url_parts[2]
path2 = url_parts[3] if len(url_parts) > 3 else ""

if domain2 == domain1 and path2.startswith(path1):
    print("link2 is a continuation of link1.")
else:
    print("link2 is unrelated to link1.")
