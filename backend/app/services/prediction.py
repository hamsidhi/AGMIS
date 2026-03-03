import statistics

class PredictionService:
    def calculate_base_score(self, metrics, weights=None):
        """
        Calculates the raw weighted score for a student without trend/momentum effects.
        Input: [lec_attn, prac_attn, assign_pct, internal, external, practical]
        """
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

        return (l_pct * w_lec) + (p_pct * w_prac) + (a_pct * w_assign) + (internal_pct * w_internal) + (external_pct * w_external)

    def predict_subject_score(self, metrics, weights=None, historical_scores=None, doubt_intensity=0):
        """
        Input: [lec_attn, prac_attn, assign_pct, internal, external, practical]
        historical_scores: list of recent scores (max 4-6) to calculate trend.
        doubt_intensity: integer count of recent tagged doubts.
        Returns: score (0-100), category, risk_tier, confidence
        """
        current_score = self.calculate_base_score(metrics, weights)
        
        # 1. Trend Analysis (Momentum)
        momentum = 0.0
        confidence = 50.0 # Base confidence for single-shot predict
        
        if historical_scores and len(historical_scores) > 0:
            # We have past data. Calculate slope.
            history = historical_scores[-4:] # Last 4 weeks
            avg_history = sum(history) / len(history)
            trend_slope = current_score - avg_history
            
            # Dampened trend to prevent infinite scaling
            if trend_slope > 5:
                momentum += 5.0
            elif trend_slope < -5:
                momentum -= 5.0
            else:
                momentum += trend_slope * 0.5 # Small momentum
                
            # Variance for confidence score
            if len(history) > 1:
                variance = statistics.stdev(history + [current_score])
                # High variance lowers confidence
                confidence_penalty = min(variance * 1.5, 30.0) 
                confidence = 85.0 - confidence_penalty + (len(history) * 2) # More data = higher confidence
            else:
                confidence = 65.0
        
        # 2. Doubt Intensity Modifier
        if doubt_intensity > 5:
            # High intensity signals confusion. We lower the prediction to act as an "early-warning" intervention cue.
            momentum -= min(doubt_intensity * 0.5, 5.0) # Up to -5 penalty
            
        future_score = current_score + momentum
        
        # Clamp score between 0 and 100
        future_score = max(0.0, min(100.0, future_score))
        confidence = max(0.0, min(100.0, confidence))
        
        # 3. Categorization & Risk Tiering
        if future_score >= 85: 
            cat = "Excellent"
            risk = "🔵 High Performer"
        elif future_score >= 70: 
            cat = "Good"
            risk = "🟢 Stable"
        elif future_score >= 55: 
            cat = "Average"
            risk = "🟡 Moderate Risk"
        elif future_score >= 40: 
            cat = "At Risk"
            risk = "🔴 High Risk"
        else: 
            cat = "Critical"
            risk = "🔴 High Risk"
            
        return {
            "score": round(future_score, 2), 
            "cat": cat,
            "risk_tier": risk,
            "confidence": round(confidence, 1)
        }

predict_service = PredictionService()
