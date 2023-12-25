#include <bits/stdc++.h>

using namespace std;

template <typename T>
struct FlowEdge {
    int u, v;
    T c, f;

    FlowEdge(int _u, int _v, T _c, T _f) :
        u(_u), v(_v), c(_c), f(_f) {}
};

template <typename T>
struct Dinic {
    static constexpr T inf = numeric_limits<T>::max();
    static constexpr T eps = (T) 1e-9;
    int n;
    int s, t;
    vector<vector<int>> adj; // stores indices of edges
    vector<int> level;       // shortest distance from source
    vector<int> ptr;         // points to the next edge which can be used
    vector<FlowEdge<T>> edges;

    Dinic(int _n, int _s, int _t)
        : n(_n), s(_s), t(_t), adj(_n), level(_n), ptr(_n) {}

    void addEdge(int u, int v, int c, int rc=0) {
        int eid = (int) edges.size();
        adj[u].push_back(eid);
        adj[v].push_back(eid + 1);
        edges.emplace_back(u, v, c, 0);
        edges.emplace_back(v, u, rc, 0);
    }

    bool bfs() {
        fill(level.begin(), level.end(), -1);
        level[s] = 0;
        queue<int> q;
        q.push(s);

        while (!q.empty()) {
            int u = q.front();
            q.pop();

            for (int eid : adj[u]) {
                const auto& e = edges[eid];
                if (e.c - e.f <= eps || level[e.v] != -1) continue;
                level[e.v] = level[u] + 1;
                q.push(e.v);
            }
        }

        return level[t] != -1;
    }

    T dfs(int u, T flow) {
        if (u == t) return flow;

        for (int& j = ptr[u]; j < (int) adj[u].size(); j++) {
            int eid = adj[u][j];
            const auto& e = edges[eid];
            if (e.c - e.f > eps && level[e.v] == level[u] + 1) {
                T df = dfs(e.v, min(e.c - e.f, flow));
                if (df > eps) {
                    edges[eid].f += df;
                    edges[eid ^ 1].f -= df;
                    return df;
                }
            }
        }

        return 0;
    }

    T maxFlow() {
        T f = 0;

        while (bfs()) {
            fill(ptr.begin(), ptr.end(), 0);
            T total_df = 0;
            while (true) {
                T df = dfs(s, inf);
                if (df <= eps) break;
                total_df += df;
            }
            if (total_df <= eps) break;
            f += total_df;
        }

        return f;
    }

    vector<int> getMinCut() {
        bfs();  // Find reachable nodes after finding maximum flow
        vector<int> cut;  // Nodes in the minimum cut

        for (int i = 0; i < n; ++i) {
            if (level[i] == -1) {
                continue;  // Unreachable
            }
            cut.push_back(i);
        }

        return cut;
    }

    T getMinCutCapacity() {
        vector<int> cut = getMinCut();
        T min_cut_cap = 0;
        for (int u : cut) {
            for (int eid : adj[u]) {
                const auto& e = edges[eid];
                if (level[e.v] == -1) {
                    // Edge going from a reachable node to an unreachable node
                    min_cut_cap += e.c;
                }
            }
        }

        return min_cut_cap;
    }
};

struct Graph {
    int n;
    vector<set<int>> adj;

    Graph(int n_) : n(n_), adj(n_) {}

    void add_edge(int u, int v) {
        adj[u].insert(v);
        adj[v].insert(u);
    }
};

int main() {
    map<string, int> nodes;
    vector<string> node_label;
    int n = 0;
    vector<pair<int, int>> edges;
    string su;
    string inp;

    while (cin >> inp) {
        string sv = "";
        string nn;
        if (inp.size() == 4) {
            su = inp.substr(0, 3);
            nn = su;
        } else {
            sv = inp;
            nn = sv;
        }
        if (nodes.find(nn) == nodes.end()) {
            nodes[nn] = n++;
            node_label.push_back(nn);
        }
        if (sv.size() > 0) {
            int u = nodes[su];
            int v = nodes[sv];
            if (u < v) {
                edges.emplace_back(u, v);
            } else {
                edges.emplace_back(v, u);
            }
        }
    }

    Graph g(n);

    for (const pair<int, int>& p : edges) {
        int u = p.first;
        int v = p.second;
        g.add_edge(u, v);
    }

    for (int s = 0; s < n; s++) {
        for (int t = 0; t < n; t++) {
            if (s == t) continue;
            Dinic<int> dinic(n, s, t);
            for (int u = 0; u < g.n; u++) {
                for (int v : g.adj[u]) {
                    dinic.addEdge(u, v, 1);
                }
            }

            int max_flow = dinic.maxFlow();
            if (max_flow == 3) {
                int k = dinic.getMinCut().size();
                int ans = k * (n - k);
                cout << ans << "\n";
                return 0;
            }
        }
    }

    return 0;
}
