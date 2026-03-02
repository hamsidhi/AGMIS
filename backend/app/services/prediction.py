class PredictionService:
    def predict_subject_score(self, metrics, weights=None):
        """
        Input: [lec_attn, prac_attn, assign_pct, internal, external, practical]
        Returns: score (0-100), category
        """
        # Manual weight calculation for subject-wise accuracy
        # Lecture (20%), Practical (10%), Assignments (10%), Internal (20%), External (40%)
        l_pct, p_pct, a_pct, i_val, e_val, pr_val = metrics
        
        # Normalize marks to percentages
        internal_pct = (i_val / 20) * 100
        external_pct = (e_val / 75) * 100
        
        if weights and all(k in weights for k in ("w_lec","w_prac","w_assign","w_internal","w_external")):
            w_lec = float(weights["w_lec"] or 0.2)
            w_prac = float(weights["w_prac"] or 0.1)
            w_assign = float(weights["w_assign"] or 0.1)
            w_internal = float(weights["w_internal"] or 0.2)
            w_external = float(weights["w_external"] or 0.4)
        else:
            w_lec, w_prac, w_assign, w_internal, w_external = 0.20, 0.10, 0.10, 0.20, 0.40

        total_w = w_lec + w_prac + w_assign + w_internal + w_external
        if total_w == 0:
            w_lec, w_prac, w_assign, w_internal, w_external = 0.20, 0.10, 0.10, 0.20, 0.40
            total_w = 1.0

        score = (l_pct * w_lec) + (p_pct * w_prac) + (a_pct * w_assign) + (internal_pct * w_internal) + (external_pct * w_external)
        
        # Refined category thresholds for better accuracy
        if score >= 85: cat = "Excellent"
        elif score >= 70: cat = "Good"
        elif score >= 55: cat = "Average"
        elif score >= 40: cat = "At Risk"
        else: cat = "Critical"
        
        return {"score": round(score, 2), "cat": cat}

predict_service = PredictionService()
