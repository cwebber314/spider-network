vm = new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    delimiters: ["{[", "]}"],
    data: {
        msg: 'Hellow Worls!',
        networks: [],
        node: null,
        nodes: [],
        network: null,
    },
    watch: {
        network: function (networkid) {
            this.getNodes(networkid)
            // this.getNetworkAll(networkid)
        },
        node: function (node) {
            console.log("Node: " + node)
            this.getNetworkPartial(this.network, node)
        }
    }, // end watch
    mounted: function () {
        this.getNetworks()
    }, // end mounted
    methods: {
        getNetworks: function () {
            axios.get('/api/list_networks').then(
                response => {
                    this.networks = response['data']
                    cy.elements().remove()
                }
            )
        }, // end getNetworks
        getNodes (networkid) {
            // Get all the nodes in the network
            // Use this for the node select autocomplete
            axios.get('/api/list_nodes/' + networkid).then(
                response => {
                    this.nodes = response['data']
                }
            )
        }, // end getNodes
        getNetworkPartial (networkid, nodeid) {
            var eles = {}
            // get network in the neighborhood of the specified node 
            axios.get('/api/get_network_partial/' + networkid + '/' + nodeid).then(
                response => {
                    var edges = []
                    var nodes = []
                    var all_eles = response['data']
                    var eles = []
                    all_eles.forEach(function (ele) {
                        if (ele['group'] == 'nodes') {
                            var e = cy.nodes('[busnum =' + ele.data['busnum'] + ']')
                            if (e.length == 0) {
                                eles.push(ele)
                            }
                        }
                        else if (ele['group'] == 'edges') {
                            var e = cy.edges('[edgeid =' + ele.data['edgeid'] + ']')
                            if (e.length == 0) {
                                eles.push(ele)    
                            }
                        }
                    })

                    cy.elements().lock()
                    console.log("Add elements")
                    console.log(eles)
                    // For the partial network we only add elements to the diagram
                    // if they don't already exist. 
                    
                    cy.add(eles)
                    var el = cy.elements().layout(layout_options).run()    
                    }
            )
        },
        getNetworkAll (networkid) {
            // get the entire network - useful for debug.
            axios.get('/api/get_network_all/' + networkid)
            .then(response => {
                var eles = response['data']
                console.log("Add elements")
                console.log(eles)
                cy.add(eles)
                cy.elements().show()
                cy.layout(layout_options).run()    
                }
            )
        },
    }, // end methods
}) // end vue

var layout_options = {
    name: 'cose',
    nodeRepulsion: 1e5,
    stop: finishLayout
}

var style = [
    {
        selector: 'node',
        style: {
            'label': 'data(label)',
        }
    },
    {
        selector: 'edge',
        style: {
            'curve-style': 'bezier',
            'label': 'data(ckt)',
        }
    },
    {
        selector: 'node[kv>100][kv<300]',
        style: {
            "background-color": "red"
        }
    },
    {
    selector: 'node[kv>50][kv<100]',
        style: {
            "background-color": "green"
        }
    },
    {
    selector: 'node[kv<50]',
        style: {
            "background-color": "pink"
        }
    },
]

var cy = cytoscape({
    container: document.getElementById('cy'),
    style: cytoscape.stylesheet(),
    elements: {},
    style: style
})

cy.on("cxttap", "node", function (e) {
    console.log("right-click handler")
    if (e.originalEvent.ctrlKey) {
        // don't actually remove it from the diagram, just hide it.
        // if we grow out again, the node keeps it's old location
        console.log("hide node")
        e.target.hide()
    } else {
        console.log("grow node" + e.target.data()['id'])
        vm.getNetworkPartial(vm.network, e.target.data()['id'])
        cy.elements().unselect()
        e.target.closedNeighborhood().show()
        // cy.$(':visible').layout(layout_options).run()
    }
})

function finishLayout() {
    cy.elements().unlock()
}