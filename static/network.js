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
            this.getNetworkAll(networkid)
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
        getNetwork (networkid, nodeid) {
            var eles = {}
            // get network in the neighborhood of the specified node 
            axios.get('/api/get_network_partial/' + networkid + '/' + nodeid).then(
                response => {
                    eles = response['data']
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
                cy.elements().remove()
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
    // nodeSpacing: 80,
    // edgeLengthVal: 45
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
    }
]

var cy = cytoscape({
    container: document.getElementById('cy'),
    style: cytoscape.stylesheet(),
    elements: {},
    style: style
})