from imports import *
def execute_queries(graph,course):
    ex = Namespace('http://example.org/ontology#')
    q1 = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
             PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
             PREFIX ex: <http://example.org/ontology/>
             PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

             SELECT ?teacher (COUNT(?skill) AS ?matchedSkillCount) 
             WHERE {{
                 ?teacher ex:hasSkill ?skill.
                 ex:{course} ex:requiresSkill ?skill.
             }}
             GROUP BY ?teacher
             ORDER BY DESC(?matchedSkillCount)"""

    q2 = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
             PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
             PREFIX ex: <http://example.org/ontology/>
             PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

             SELECT ?teacher (COUNT(?role) AS ?matchedCount)  
             WHERE {{
                 ?teacher ex:hasExperience ?exp.
                 ?exp ex:hasRole ?role.
                 ?role ex:roleRelevantTo ex:{course}.
             }}
             GROUP BY ?teacher
             ORDER BY DESC(?matchedCount)"""

    q3 = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
             PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
             PREFIX ex: <http://example.org/ontology/>
             PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

             SELECT ?teacher (SUM(?years) AS ?totalYears) (COUNT(?role) AS ?matchedCount)  
             WHERE {{
                 ?teacher ex:hasExperience ?exp.
                 ?exp ex:hasRole ?role.
                 ?role ex:roleRelevantTo ex:{course}.
                 ?exp ex:yearsOfExperience ?years.
             }}
             GROUP BY ?teacher
             ORDER BY DESC(?totalYears)"""

    q4 = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
             PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
             PREFIX ex: <http://example.org/ontology/>
             PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

             SELECT ?teacher (COUNT(?research) AS ?matchedCount)  
             WHERE {{
                 ?teacher ex:doneResearch ?research.
                 ?research ex:researchRelatedTo ex:{course}.
             }}
             GROUP BY ?teacher
             ORDER BY DESC(?matchedCount)"""

    q5 = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
             PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
             PREFIX ex: <http://example.org/ontology/>
             PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

             SELECT ?teacher (COUNT(?domain) AS ?matchedCount)  
             WHERE {{
                 ?teacher ex:relatedToDomain ?domain.
                 ex:{course} ex:belongsToDomain ?domain.
             }}
             GROUP BY ?teacher
             ORDER BY DESC(?matchedCount)"""

    q6 = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
             PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
             PREFIX ex: <http://example.org/ontology/>
             PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

             SELECT ?teacher (COUNT(?degree) AS ?matchedCount)  
             WHERE {{
                 ?teacher ex:hasDegree ?degree.
                 ex:{course} ex:requiresDegree ?degree.
             }}
             GROUP BY ?teacher
             ORDER BY DESC(?matchedCount)"""

    scores = {}
    results = graph.query(q1)
    for result in results:
        teacher = str(result.teacher).split("/")[-1]
        matched_skills = int(result.matchedSkillCount)
        if teacher not in scores:
            scores[teacher] = {"matchedSkills": 0, "jobExperience": 0, "weightedExperience": 0, "researchExperience": 0, "domainMatching": 0, "degreeMatching": 0}
        scores[teacher]["matchedSkills"] = matched_skills

    results = graph.query(q2)
    for result in results:
        teacher = str(result.teacher).split("/")[-1]
        matched_exp = int(result.matchedCount)
        if teacher not in scores:
            scores[teacher] = {"matchedSkills": 0, "jobExperience": 0, "weightedExperience": 0, "researchExperience": 0, "domainMatching": 0, "degreeMatching": 0}
        scores[teacher]["jobExperience"] = matched_exp

    results = graph.query(q3)
    for result in results:
        teacher = str(result.teacher).split("/")[-1]
        total_years = int(result.totalYears)
        if teacher not in scores:
            scores[teacher] = {"matchedSkills": 0, "jobExperience": 0, "weightedExperience": 0, "researchExperience": 0, "domainMatching": 0, "degreeMatching": 0}
        scores[teacher]["weightedExperience"] = total_years

    results = graph.query(q4)
    for result in results:
        teacher = str(result.teacher).split("/")[-1]
        matched_research = int(result.matchedCount)
        if teacher not in scores:
            scores[teacher] = {"matchedSkills": 0, "jobExperience": 0, "weightedExperience": 0, "researchExperience": 0, "domainMatching": 0, "degreeMatching": 0}
        scores[teacher]["researchExperience"] = matched_research

    results = graph.query(q5)
    for result in results:
        teacher = str(result.teacher).split("/")[-1]
        matched_domains = int(result.matchedCount)
        if teacher not in scores:
            scores[teacher] = {"matchedSkills": 0, "jobExperience": 0, "weightedExperience": 0, "researchExperience": 0, "domainMatching": 0, "degreeMatching": 0}
        scores[teacher]["domainMatching"] = matched_domains

    results = graph.query(q6)
    for result in results:
        teacher = str(result.teacher).split("/")[-1]
        matched_degrees = int(result.matchedCount)
        if teacher not in scores:
            scores[teacher] = {"matchedSkills": 0, "jobExperience": 0, "weightedExperience": 0, "researchExperience": 0, "domainMatching": 0, "degreeMatching": 0}
        scores[teacher]["degreeMatching"] = matched_degrees

    df = pd.DataFrame.from_dict(scores, orient="index")
    df.index.name = "Teacher"
    df.reset_index(inplace=True)
    df['Score'] = df["matchedSkills"] + df["jobExperience"] + df["weightedExperience"] + df["researchExperience"] + df["domainMatching"] + df["degreeMatching"]
    best_teacher = df[df["Score"] == df["Score"].max()]["Teacher"].values[0]

    q1_1 = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
               PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
               PREFIX ex: <http://example.org/ontology/>
               PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

               SELECT ?skill
               WHERE {{
                   ex:{best_teacher} ex:hasSkill ?skill.
                   ex:{course} ex:requiresSkill ?skill.
               }}"""

    q2_1 = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
               PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
               PREFIX ex: <http://example.org/ontology/>
               PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

               SELECT ?exp ?role ?years ?organization
               WHERE {{
                   ex:{best_teacher} ex:hasExperience ?exp.
                   ?exp ex:hasRole ?role.
                   ?role ex:roleRelevantTo ex:{course}.
                   ?exp ex:yearsOfExperience ?years. 
                   ?exp ex:organization ?organization.
               }}"""

    q3_1 = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
               PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
               PREFIX ex: <http://example.org/ontology/>
               PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

               SELECT ?research
               WHERE {{
                   ex:{best_teacher} ex:doneResearch ?research.
                   ?research ex:researchRelatedTo ex:{course}.
               }}"""

    q4_1 = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
               PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
               PREFIX ex: <http://example.org/ontology/>
               PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

               SELECT ?domain
               WHERE {{
                   ex:{best_teacher} ex:relatedToDomain ?domain.
                   ex:{course} ex:belongsToDomain ?domain.
               }}"""

    q5_1 = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
               PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
               PREFIX ex: <http://example.org/ontology/>
               PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

               SELECT ?degree
               WHERE {{
                   ex:{best_teacher} ex:hasDegree ?degree.
                   ex:{course} ex:requiresDegree ?degree.
               }}"""

    skills = []
    ans = graph.query(q1_1)
    for t in ans:
        skills.append(str(t.skill).split("/")[-1])

    relevant_experiences = []
    ans = graph.query(q2_1)
    for t in ans:
        role = str(t.role).split("/")[-1]
        organization = str(t.organization).split("/")[-1]
        relevant_experiences.append([role, int(t.years), organization])

    research_work = []
    ans = graph.query(q3_1)
    for t in ans:
        research_work.append(str(t.research).split("/")[-1])

    depart_domain = []
    ans = graph.query(q4_1)
    for t in ans:
        depart_domain.append(str(t.domain).split("/")[-1])

    degrees = []
    ans = graph.query(q5_1)
    for t in ans:
        degrees.append(str(t.degree).split("/")[-1])

    return best_teacher, skills, relevant_experiences, research_work, depart_domain, degrees, df