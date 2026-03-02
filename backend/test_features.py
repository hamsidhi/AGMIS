from app.services.features import feature_service

# Mock data for a struggling student
attendance = 60.0
internals = 55.0
assignments = 40.0

score = feature_service.calculate_weighted_score(attendance, internals, assignments)
category = feature_service.get_performance_category(score)

print(f"Weighted Score: {score}")
print(f"Category: {category}")

# Should match PRD: score ~53.0, Category: At Risk