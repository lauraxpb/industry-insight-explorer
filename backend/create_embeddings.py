from database import industries_collection
from embeddings import generate_embeddings

industries = list(
    industries_collection.find({}, {"_id": 1, "name": 1, "description": 1})
)

texts = [
    f"{ind['name']}. {ind.get('description', '')}"
    for ind in industries
]

embeddings = generate_embeddings(texts)

for industry, embedding in zip(industries, embeddings):
    industries_collection.update_one(
        {"_id": industry["_id"]},
        {"$set": {"embedding": embedding}}
    )

print("Industry embeddings created")
print("Industries fetched:", industries)
print("Embeddings fetched:", embeddings)