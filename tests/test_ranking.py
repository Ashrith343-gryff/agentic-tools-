from decider.ranking import rank_candidates


def test_rank_candidates_knowledge(sample_tool_candidates):
    request = "Find information about MCP in the workshop documents"
    ranked, scores = rank_candidates(request, sample_tool_candidates)

    assert len(ranked) == 3
    # search_knowledge should be ranked highest
    assert ranked[0].name == "search_knowledge"
    assert scores["search_knowledge"] > scores["calculator"]


def test_rank_candidates_calculator(sample_tool_candidates):
    request = "Calculate 12 * 5"
    ranked, scores = rank_candidates(request, sample_tool_candidates)

    assert ranked[0].name == "calculator"


def test_rank_candidates_ties(sample_tool_candidates):
    request = "Unrelated request that matches no heuristics"
    ranked, scores = rank_candidates(request, sample_tool_candidates)

    # All scores should be 0.0
    for score in scores.values():
        assert score == 0.0

    # Order should be stable (alphabetical by name: calculator, search_knowledge, sqlite_query)
    assert ranked[0].name == "calculator"
    assert ranked[1].name == "search_knowledge"
    assert ranked[2].name == "sqlite_query"


def test_rank_candidates_empty():
    ranked, scores = rank_candidates("Find something", [])
    assert ranked == []
    assert scores == {}
