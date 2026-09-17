from rag.retriever import retrieve

def generate_recommendations(slots):
    recommendations = []
    
    # Extract variables with fallbacks
    ph = slots.get('soil_ph', 7.0)
    soc = slots.get('organic_carbon_pct', 1.0)
    rainfall = slots.get('rainfall_mm', 800)
    land_use = slots.get('land_use', 'unknown').lower()
    species = slots.get('species_richness', 50)
    pollution = slots.get('pollution_level', 'medium')
    moisture = slots.get('moisture', 'medium')
    habitat = slots.get('habitat_diversity', 'medium')
    region = slots.get('region', 'unknown').lower()

    # Rule 1: Semi-Arid + Monoculture + Low SOC (Matches company's example)
    if region == 'semi-arid' and 'monoculture' in land_use and soc < 1.0:
        recommendations.append({
            "recommendation": "Adopt agroforestry / intercropping with native trees",
            "why": "Integrating trees into monoculture systems increases soil carbon through leaf litter and root exudates. It also creates microclimates that support pollinators. Studies show agroforestry can increase SOC by 10-20% and species richness by up to 30%.",
            "metrics_improved": ["soil organic carbon", "habitat diversity", "pollinator support"],
            "time_horizon": "long (3-5 years)",
            "confidence": "High",
            "evidence": [
                {"source": "FAO", "year": 2017, "url": "https://openknowledge.fao.org"},
                {"source": "IPCC", "year": 2019, "url": "https://www.ipcc.ch/report/srccl/"}
            ]
        })

    # Rule 2: Acidic soil + Low SOC + High Rainfall
    if ph < 6.0 and soc < 1.0 and rainfall > 1000:
        recommendations.append({
            "recommendation": "Apply agricultural lime combined with compost",
            "why": "Low pH reduces nutrient availability. Liming raises pH, while compost adds organic carbon. This can improve microbial diversity by 20-30% within 1 year.",
            "metrics_improved": ["soil pH", "soil organic carbon", "microbial diversity"],
            "time_horizon": "medium (1-2 years)",
            "confidence": "High",
            "evidence": [{"source": "FAO", "year": 2017, "url": "https://openknowledge.fao.org"}]
        })

    # Rule 3: High pH + Low SOC + Monoculture
    if ph > 7.5 and soc < 1.0 and "monoculture" in land_use:
        recommendations.append({
            "recommendation": "Introduce legume-based cover crops",
            "why": "Legumes fix nitrogen and increase soil organic carbon by ~15-25% over 2-3 years, improving microbial diversity and pollinator support.",
            "metrics_improved": ["soil organic carbon", "microbial diversity", "pollinator support"],
            "time_horizon": "medium (2-3 years)",
            "confidence": "High",
            "evidence": [{"source": "FAO", "year": 2017, "url": "https://openknowledge.fao.org"}]
        })

    # Rule 4: Low Rainfall + Low Species Richness + Low Moisture
    if rainfall < 700 and species < 20 and moisture == 'low':
        recommendations.append({
            "recommendation": "Create water harvesting structures (check dams, contour trenches)",
            "why": "Improves soil moisture by up to 40%, supports vegetation, and increases habitat for insects and birds.",
            "metrics_improved": ["soil moisture", "species richness", "habitat diversity"],
            "time_horizon": "short (6-12 months)",
            "confidence": "Medium",
            "evidence": [{"source": "IPBES", "year": 2019, "url": "https://ipbes.net"}]
        })

    # Rule 5: High Pollution + Low Habitat Diversity + Cropland
    if pollution == 'high' and habitat == 'low' and 'crop' in land_use:
        recommendations.append({
            "recommendation": "Plant native riparian buffers along water bodies",
            "why": "Filters agricultural runoff, reduces water pollution by 30-50%, and creates wildlife corridors.",
            "metrics_improved": ["water quality", "aquatic species survival", "habitat connectivity"],
            "time_horizon": "long (3-5 years)",
            "confidence": "High",
            "evidence": [{"source": "IUCN", "year": 2020, "url": "https://iucn.org"}]
        })

    return recommendations