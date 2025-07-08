from services.rollback_engine.decision import should_rollback


risk_score = 0.8

rollback, reason = should_rollback(risk_score)

print(" Should rollback:", rollback)
print(" Reason:", reason)
