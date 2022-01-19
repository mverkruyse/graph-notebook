"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""
import pytest

from graph_notebook.network.gremlin.GremlinNetwork import GremlinNetwork, PathPattern

from test.integration import DataDrivenGremlinTest


class TestGremlinNetwork(DataDrivenGremlinTest):

    @pytest.mark.gremlin
    def test_add_path_with_edge_object(self):
        query = "g.V().has('airport','code','AUS').outE().inV().path().by('code').by().limit(10)"
        results = self.client.gremlin_query(query)
        gn = GremlinNetwork()
        pattern = [PathPattern.V, PathPattern.OUT_E, PathPattern.IN_V]
        gn.add_results_with_pattern(results, pattern)
        self.assertEqual(11, len(gn.graph.nodes))
        self.assertEqual(10, len(gn.graph.edges))

    @pytest.mark.gremlin
    def test_add_path_by_dist(self):
        query = """g.V().has('airport','code','AUS').
          repeat(outE().inV().simplePath()).
          until(has('code','WLG')).
          limit(5).
          path().
            by('code').
            by('dist')"""
        results = self.client.gremlin_query(query)
        gn = GremlinNetwork()
        pattern = [PathPattern.V, PathPattern.OUT_E, PathPattern.IN_V, PathPattern.OUT_E]
        gn.add_results_with_pattern(results, pattern)
        self.assertEqual(8, len(gn.graph.nodes))
        self.assertEqual(11, len(gn.graph.edges))

    @pytest.mark.gremlin
    def test_path_with_dict(self):
        query = """g.V().has('airport','code','CZM').
                      out('route').
                      path().
                        by(valueMap('code','city','region','desc','lat','lon').
                           order(local).
                             by(keys))"""
        results = self.client.gremlin_query(query)
        gn = GremlinNetwork()
        pattern = [PathPattern.V, PathPattern.IN_V]
        gn.add_results_with_pattern(results, pattern)
        self.assertEqual(12, len(gn.graph.nodes))
        self.assertEqual(11, len(gn.graph.edges))
