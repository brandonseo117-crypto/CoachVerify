SPORTS_SCIENCE_DB = {
    "dry_scooping": {
        "title": "Social Media Trends, Dry Scooping, and Extensive Esophageal Ulcerations",
        "consensus": "Highly Unsafe. Ingesting multi-ingredient pre-workout powders (MIPS) without recommended solvents prevents complete powder dissolution, creating localized pockets of dry matter. This leads to prolonged esophageal transit times and caustic, structural mucosal contact, inducing severe punctate and deep linear esophageal ulcerations, severe odynophagia, and gastric erosions.",
        "base_safety": 10,
        "base_performance": 50,
        "pubmed_link": r"https://pubmed.ncbi.nlm.nih.gov/37758968/",
        "methodology": {
            "study_type": "Clinical Case Report & Histopathological Evaluation",
            "sample_size": 1,
            "journal_authority": "Journal of General Internal Medicine (JGIM)",
            "year": 2023,
            "population_demographics": "22-year-old competitive male weightlifter presenting with acute dysphagia and odynophagia"
        }
    },
    "dry_scooping_prevalence": {
        "title": "Prevalence and Correlates of Dry Scooping Among Canadian Adolescents and Young Adults",
        "consensus": r"Common behavior with high psychological correlation. Approximately 16.9% of youth fitness consumers engage in dry scooping, with occurrence rising significantly to 21.8% among men. Strong correlation exists between this practice and excessive social media consumption, intensive weight training, and clinical indicators of muscle dysmorphia, presenting compounding risks of accidental powder inhalation, digestive caustic lesions, and acute caffeine cardiotoxicity.",
        "base_safety": 25,
        "base_performance": 40,
        # Extracted standard lookup for this exact 2022 study
        "pubmed_link": "https://pubmed.ncbi.nlm.nih.gov/36764046/",
        "methodology": {
            "study_type": "National Epidemiological Survey & Cross-Sectional Poisson Regression Analysis",
            "sample_size": 2731,
            "journal_authority": "Eating Behaviors / Canadian Study of Adolescent Health Behaviors",
            "year": 2022,
            "population_demographics": "Canadian adolescents and young adults aged 16-30 (54.3% women, 39.0% men, 6.7% TGNC)"
        }
    },
    "dry_scooping_cardiac": {
        "title": "Acute myocardial infarction following 'dry scooping' of a pre-workout supplement in a healthy young man of African origin: A case report",
        "consensus": r"Critically Dangerous. Ingesting concentrated, undiluted pre-workout powder triggers a rapid surge of sympathomimetic stimulants (high-dose caffeine and synephrine) into the bloodstream without a fluid canvas. This induces acute coronary vasospasm, extreme sympathetic activation, and hypercoagulability, precipitating severe transmural anterolateral ST-elevation myocardial infarction (acute heart attack) and coronary thrombosis, even in young, healthy individuals with no prior history of cardiovascular disease.",
        "base_safety": 5,
        "base_performance": 45,
        # Official PMID index mapping for this 2024 SAGE publication
        "pubmed_link": r"https://pmc.ncbi.nlm.nih.gov/articles/PMC11179451/",
        "methodology": {
            "study_type": "Clinical Case Report & Emergency Coronary Angiography Analysis",
            "sample_size": 1,
            "journal_authority": "SAGE Open Medical Case Reports",
            "year": 2024,
            "population_demographics": "Previously healthy 25-year-old male athlete presenting with crushing mid-sternal chest pain following a 2-hour workout"
        }
    },
    "mouth_taping_systematic_review": {
        "title": r"Breaking social media fads and uncovering the safety and efficacy of mouth taping in patients with mouth breathing, sleep disordered breathing, or obstructive sleep apnea: A systematic review",
        "consensus": r"Unverified performance fad with elevated risk profiles. Systematic literature evaluation reveals that prominent social media claims celebrating nocturnal mouth taping for athletic recovery, enhanced immunity, and structural facial changes are completely unsupported by high-quality empirical evidence. While it may show minor, heterogeneous reductions in mild snoring or open-mouth leaks during sleep, it introduces critical safety hazards including acute upper airway resistance, severe local skin irritation from chemical adhesives, and extreme risks of suffocation or aspiration in individuals with undiagnosed severe obstructive sleep apnea (OSA) or nasal congestion.",
        "base_safety": 35,
        "base_performance": 20,
        # Clean cross-reference string mapping
        "pubmed_link": r"https://pmc.ncbi.nlm.nih.gov/articles/PMC12094774/",
        "methodology": {
            "study_type": r"Systematic Literature Review & Multi-Database Quality Assessment",
            # Aggregated patient pools meeting strict systematic trial entry parameters
            "sample_size": 268,
            "journal_authority": r"PLoS One",
            "year": 2025,
            "population_demographics": r"Heterogeneous cohorts across multiple clinical trials presenting with mouth breathing, snoring, or sleep-disordered breathing"
        }
    },

    "mouth_taping_social_media": {
        "title": r"Nocturnal mouth-taping and social media: A scoping review of the evidence",
        "consensus": r"High-risk algorithmic trend driven by low-quality information. A scoping analysis cross-examining peer-reviewed data against viral TikTok content confirms a severe disconnect: over 91.5% of high-engagement social media videos promote nocturnal mouth taping as a miraculous cure-all for sleep quality and sports recovery, yet completely fail to declare critical medical contraindications. The clinical reality indicates that forcing nasal breathing via mechanical tape obstruction without pre-screening nasal airway patency or internal upper airway anatomy can cause hypoxic drops, hypercapnia (carbon dioxide retention), and significant sleep architecture disruption.",
        "base_safety": 40,
        "base_performance": 15,
        "pubmed_link": r"https://www.sciencedirect.com/science/article/pii/S0196070924003314?ref=pdf_download&fr=RR-2&rr=a0e6904b2c28fbf2",
        "methodology": {
            "study_type": r"Scoping Review & Social Media Content Quality Framework Analysis",
            # Includes combined analysis of clinical papers alongside qualitative high-yield social videos
            "sample_size": 112,
            "journal_authority": r"American Journal of Otolaryngology",
            "year": 2025,
            "population_demographics": r"Scholastic fitness consumers exposed to digital wellness trends alongside monitored clinical sleep cohorts"
        }
    },

    "mouth_taping_clinical_trial": {
        "title": r"The Impact of Mouth-Taping in Mouth-Breathers with Mild Obstructive Sleep Apnea: A Preliminary Study",
        "consensus": r"Potentially beneficial ONLY for mild, pre-screened structural conditions under strict medical supervision. Monitored polysomnography tracking reveals that a porous silicone patch (porous mouth-taping) can successfully shift breathing routing to the nose, yielding a significant decrease in the apnea-hypopnea index (AHI) and reducing snoring frequency by up to 47% in dedicated mouth-breathers. However, these specific positive parameters are completely restricted to individuals with strictly MILD obstructive sleep apnea and absolute nasal airway clearance; it remains highly dangerous for standard un-screened athletes with structural nasal collapses.",
        "base_safety": 65,
        "base_performance": 55,
        "pubmed_link": r"https://pmc.ncbi.nlm.nih.gov/articles/PMC9498537/",
        "methodology": {
            "study_type": r"Prospective Interventional Cohort Study & Sleep Laboratory Polysomnography Audit",
            "sample_size": 20,
            "journal_authority": r"Healthcare (MDPI)",
            "year": 2022,
            "population_demographics": r"Adult mouth-breathers diagnosed with mild obstructive sleep apnea (AHI between 5 and 15)"
        }
    },

    "bench_press_failure_2005": {
        "title": r"Training leading to repetition failure enhances bench press strength gains in elite junior athletes",
        "consensus": r"Highly effective for rapid upper-body strength and ballistic power adaptation. For elite junior team-sport athletes, structuring high-density training clusters that intentionally force mechanical repetition failure (e.g., 4 sets of 6 repetitions) yields significantly greater absolute bench press strength gains (+9.5%) and explosive bench throw power outputs (+10.6%) compared to volume-equated intra-set rest or non-failure configurations.",
        "base_safety": 75,
        "base_performance": 85,
        "pubmed_link": r"https://pubmed.ncbi.nlm.nih.gov/15903379/",
        "methodology": {
            "study_type": r"Randomized Controlled Equal-Volume Interventional Trial",
            "sample_size": 26,
            "journal_authority": r"The Journal of Strength and Conditioning Research",
            "year": 2005,
            "population_demographics": r"Elite junior male basketball and soccer players (ages 17-18) with >6 months of strength training history"
        }
    },

    "leg_extension_failure_2020": {
        "title": r"Effect of resistance training to muscle failure vs non-failure on strength, hypertrophy and muscle architecture in trained individuals",
        "consensus": r"Equally effective for hypertrophy and strength, with distinct neuromuscular efficiency benefits for non-failure. In resistance-trained individuals, training to complete muscle failure is NOT mandatory to maximize muscle cross-sectional area (CSA) or 1-RM strength, provided overall training volume is sufficient. Both protocols trigger significant, similar vastus lateralis hypertrophy (Failure: +13.5% vs. Non-Failure: +18.1%) and pennation angle changes, but non-failure training achieves these identical gains with lower neuromuscular fatigue and higher mechanical efficiency.",
        "base_safety": 80,
        "base_performance": 80,
        "pubmed_link": r"https://pmc.ncbi.nlm.nih.gov/articles/PMC7725035/",
        "methodology": {
            "study_type": r"Randomized Within-Subjects Controlled Trial (Contralateral Limb Design)",
            "sample_size": 14,
            "journal_authority": r"Biology of Sport",
            "year": 2020,
            "population_demographics": r"Resistance-trained individuals (mean age ~24.6 years) tracking independent unilateral lower-limb protocols over 10 weeks"
        }
    },

    "near_failure_motor_unit_2023": {
        "title": r"The effects of resistance training to near failure on strength, hypertrophy, and motor unit adaptations in previously trained adults",
        "consensus": r"Near-failure or failure training modifies long-term motor unit firing behavior. Modern high-density electromyographic (HD-EMG) decomposition reveals that while training to absolute or near-failure (0–1 Repetitions in Reserve) yields similar absolute 1-RM strength and vastus lateralis thickness gains to non-failure training (4–6 Repetitions in Reserve), it induces unique neural changes, specifically decreasing the average motor unit firing rates during post-testing. This indicates a profound long-term neural optimization and motor unit coordination shift unique to heavy fatigue tracking.",
        "base_safety": 75,
        "base_performance": 82,
        "pubmed_link": r"https://physoc.onlinelibrary.wiley.com/doi/10.14814/phy2.15679",
        "methodology": {
            "study_type": r"Parallel-Group Randomized Controlled Interventional Trial with HD-EMG Decomposition",
            # Reflects the completed cohort analyzed across the failure/non-failure arms
            "sample_size": 28,
            "journal_authority": r"Physiological Reports",
            "year": 2023,
            "population_demographics": r"Previously resistance-trained young adults (ages 18-35) undergoing a high-volume 8-week barbell squat and leg extension protocol"
        }
    },
    "Ghkcu": {
        "title": "The Human Tripeptide GHK-Cu in Prevention of Oxidative Stress and Degenerative Conditions",
        "journal": "Biomedicines",
        "pubmed_link": r"https://pmc.ncbi.nlm.nih.gov/articles/PMC3359723/",
        "paper_reliability": 90,
        "study_type": r"Literature Review and Biochemical Analysis",
        "publication_year": r"2024",
        "sample_size": r"N/A (Systematic Analysis)",
        "target_cohort": r"Adult cellular tissues tracking tissue regeneration and antioxidant expression",
        "consensus": r"GHK-Cu demonstrates strong tissue-remodeling and antioxidant benefits that support healthy recovery in fully mature adult systems. However, because it actively alters gene expression and growth-factor pathways, introducing this peptide into developing teenage bodies carries unpredictable systemic risks. Minors should strictly avoid it, as their hormones and growth plates are still naturally regulating.",
        "alternative": r"Focus on high-quality sleep cycles, structured progressive overload, and a balanced whole-foods protein intake to maximize natural growth hormone and recovery."
    },
    "ghkcu2": {
        "title": "Regenerative and Protective Actions of the GHK-Cu Peptide in Light of the New Gene Data",
        "journal": "International Journal of Molecular Sciences",
        "pubmed_link": r"https://pmc.ncbi.nlm.nih.gov/articles/PMC6073405/",
        "paper_reliability": 88,
        "study_type": "Gene Expression Dataset Analysis",
        "publication_year": r"2018",
        "sample_size": r"N/A (Broad Genomic Profiling)",
        "target_cohort": "Human genomic data modeling adult cellular health and collagen synthesis",
        "consensus": "Data shows that GHK-Cu resets human genes to a healthier, more regenerative state to improve collagen production and lung protection in adults. For minors under 18, artificially overriding gene pathways during critical developmental years is highly unsafe and can disrupt natural internal balances.",
        "alternative": "Utilize targeted stretching, tissue foam rolling, and adequate hydration to optimize natural muscle building and collagen synthesis safely."
    },
    "ghkcu3": {
        "title": "GHK Peptide as a Natural Modulator of Multiple Cellular Pathways in Skin Regeneration",
        "journal": "Cells",
        "pubmed_link": r"https://pmc.ncbi.nlm.nih.gov/articles/PMC4508379/",
        "paper_reliability": 85,
        "study_type": r"In Vitro Cellular Study",
        "publication_year": r"2020",
        "sample_size": r"Multiple Cellular Batches",
        "target_cohort": r"Human dermal fibroblasts tracking anti-inflammatory signaling",
        "consensus": r"This study highlights how GHK-Cu safely speeds up wound healing and lowers inflammation in adult skin cells. However, because it directly manipulates cellular signaling, it is classified as unsafe for minors whose immune systems, organs, and tissues are still undergoing natural developmental maturity.",
        "alternative": r"Rely on standard, clean topical formulations like zinc oxide or simple aloe vera matrices for localized skin healing and barrier protection."
    }

}
