var cy = window.cy = cytoscape({
    container: document.getElementById('cy'),
    minZoom: 1e-1,
    maxZoom: 1e1,
    userZoomingEnabled: true,
    pan: { x: 0, y: 0 },
    userPanningEnabled: true,
    selectionType: 'additive',
    autolock: false,
    autounselectify: true,

    style: [
        {
            selector: 'node',
            style: {
                'label': 'data(id)',
                'text-opacity': 0.7,
                'text-valign': 'center',
                'text-halign': 'center',
                'background-color': '#43CD80',
                'color': '#0D0D0D',
                'border-width':'1px',
                'border-style':'solid',
                'border-color':'black'
            },
            tytle: 'data(type)'
        },
        {
            selector: 'edge',
            style: {
                'curve-style': 'bezier',
                'width': 3,
                'target-arrow-shape': 'triangle',
                'line-color': '#E9967A',
                'target-arrow-color': '#9dbaea'
            }
        },
        {
            selector: ':selected',
            style:{
                'background-color': 'black',
                'opacity':1
            }
        }
    ],
    elements: {'nodes': [{'data': {'id': '13', 'type': 'redundancy'}}, {'data': {'id': '14', 'type': 'redundancy'}}, {'data': {'id': '15', 'type': 'redundancy'}}, {'data': {'id': '16', 'type': 'redundancy'}}, {'data': {'id': '17', 'type': 'redundancy'}}, {'data': {'id': '18', 'type': 'redundancy'}}, {'data': {'id': '19', 'type': 'redundancy'}}, {'data': {'id': '20', 'type': 'redundancy'}}, {'data': {'id': '21', 'type': 'redundancy'}}, {'data': {'id': '22', 'type': 'mutation'}}, {'data': {'id': '23', 'type': 'mutation'}}, {'data': {'id': '24', 'type': 'mutation'}}, {'data': {'id': '25', 'type': 'redundancy'}}, {'data': {'id': '26', 'type': 'mutation'}}, {'data': {'id': '27', 'type': 'mutation'}}, {'data': {'id': '28', 'type': 'redundancy'}}, {'data': {'id': '29', 'type': 'mutation'}}, {'data': {'id': '30', 'type': 'redundancy'}}, {'data': {'id': '31', 'type': 'redundancy'}}, {'data': {'id': '32', 'type': 'redundancy'}}, {'data': {'id': '33', 'type': 'redundancy'}}, {'data': {'id': '34', 'type': 'mutation'}}, {'data': {'id': '35', 'type': 'redundancy'}}, {'data': {'id': '36', 'type': 'redundancy'}}, {'data': {'id': '38', 'type': 'non-mutation'}}, {'data': {'id': '39', 'type': 'redundancy'}}, {'data': {'id': '40', 'type': 'mutation'}}, {'data': {'id': '41', 'type': 'mutation'}}, {'data': {'id': '42', 'type': 'mutation'}}, {'data': {'id': '43', 'type': 'mutation'}}, {'data': {'id': '44', 'type': 'mutation'}}, {'data': {'id': '45', 'type': 'non-mutation'}}, {'data': {'id': '46', 'type': 'redundancy'}}, {'data': {'id': '47', 'type': 'mutation'}}, {'data': {'id': '48', 'type': 'mutation'}}, {'data': {'id': '49', 'type': 'non-mutation'}}, {'data': {'id': '50', 'type': 'mutation'}}, {'data': {'id': '51', 'type': 'redundancy'}}, {'data': {'id': '52', 'type': 'mutation'}}, {'data': {'id': '53', 'type': 'mutation'}}, {'data': {'id': '54', 'type': 'mutation'}}, {'data': {'id': '55', 'type': 'non-mutation'}}, {'data': {'id': '56', 'type': 'redundancy'}}, {'data': {'id': '57', 'type': 'non-mutation'}}, {'data': {'id': '58', 'type': 'mutation'}}, {'data': {'id': '60', 'type': 'non-mutation'}}, {'data': {'id': '61', 'type': 'mutation'}}, {'data': {'id': '62', 'type': 'mutation'}}, {'data': {'id': '63', 'type': 'mutation'}}, {'data': {'id': '64', 'type': 'mutation'}}, {'data': {'id': '65', 'type': 'mutation'}}, {'data': {'id': '66', 'type': 'non-mutation'}}, {'data': {'id': '67', 'type': 'non-mutation'}}, {'data': {'id': '68', 'type': 'redundancy'}}, {'data': {'id': '69', 'type': 'mutation'}}, {'data': {'id': '70', 'type': 'mutation'}}, {'data': {'id': '71', 'type': 'mutation'}}, {'data': {'id': '72', 'type': 'mutation'}}, {'data': {'id': '73', 'type': 'mutation'}}, {'data': {'id': '74', 'type': 'mutation'}}, {'data': {'id': '75', 'type': 'redundancy'}}, {'data': {'id': '76', 'type': 'mutation'}}, {'data': {'id': '77', 'type': 'mutation'}}, {'data': {'id': '78', 'type': 'mutation'}}, {'data': {'id': '79', 'type': 'mutation'}}, {'data': {'id': '80', 'type': 'mutation', 'label': 'seed'}}, {'data': {'id': '81', 'type': 'mutation'}}, {'data': {'id': '83', 'type': 'redundancy'}}, {'data': {'id': '84', 'type': 'redundancy'}}, {'data': {'id': '85', 'type': 'mutation'}}, {'data': {'id': '86', 'type': 'mutation'}}], 'edges': [{'data': {'source': '79', 'target': '80', 'type': 'activation'}}, {'data': {'source': '80', 'target': '77', 'type': 'activation'}}, {'data': {'source': '65', 'target': '63', 'type': 'activation'}}, {'data': {'source': '40', 'target': '41', 'type': 'activation'}}, {'data': {'source': '47', 'target': '46', 'type': 'activation'}}, {'data': {'source': '46', 'target': '41', 'type': 'inhibition'}}, {'data': {'source': '77', 'target': '69', 'type': 'activation'}}, {'data': {'source': '60', 'target': '57', 'type': 'activation'}}, {'data': {'source': '28', 'target': '25', 'type': 'activation'}}, {'data': {'source': '25', 'target': '21', 'type': 'activation'}}, {'data': {'source': '23', 'target': '20', 'type': 'activation'}}, {'data': {'source': '18', 'target': '17', 'type': 'activation'}}, {'data': {'source': '78', 'target': '80', 'type': 'inhibition'}}, {'data': {'source': '78', 'target': '77', 'type': 'inhibition'}}, {'data': {'source': '75', 'target': '80', 'type': 'inhibition'}}, {'data': {'source': '74', 'target': '80', 'type': 'inhibition'}}, {'data': {'source': '73', 'target': '76', 'type': 'inhibition'}}, {'data': {'source': '71', 'target': '69', 'type': 'inhibition'}}, {'data': {'source': '68', 'target': '69', 'type': 'inhibition'}}, {'data': {'source': '69', 'target': '66', 'type': 'inhibition'}}, {'data': {'source': '45', 'target': '63', 'type': 'inhibition'}}, {'data': {'source': '39', 'target': '41', 'type': 'inhibition'}}, {'data': {'source': '44', 'target': '63', 'type': 'inhibition'}}, {'data': {'source': '38', 'target': '41', 'type': 'inhibition'}}, {'data': {'source': '42', 'target': '41', 'type': 'activation'}}, {'data': {'source': '43', 'target': '41', 'type': 'activation'}}, {'data': {'source': '43', 'target': '63', 'type': 'activation'}}, {'data': {'source': '64', 'target': '65', 'type': 'activation'}}, {'data': {'source': '64', 'target': '66', 'type': 'inhibition'}}, {'data': {'source': '64', 'target': '63', 'type': 'activation'}}, {'data': {'source': '76', 'target': '77', 'type': 'activation'}}, {'data': {'source': '61', 'target': '72', 'type': 'activation'}}, {'data': {'source': '61', 'target': '69', 'type': 'activation'}}, {'data': {'source': '61', 'target': '66', 'type': 'activation'}}, {'data': {'source': '61', 'target': '62', 'type': 'activation'}}, {'data': {'source': '61', 'target': '63', 'type': 'activation'}}, {'data': {'source': '48', 'target': '61', 'type': 'activation'}}, {'data': {'source': '69', 'target': '70', 'type': 'activation'}}, {'data': {'source': '67', 'target': '69', 'type': 'activation'}}, {'data': {'source': '66', 'target': '67', 'type': 'activation'}}, {'data': {'source': '48', 'target': '63', 'type': 'activation'}}, {'data': {'source': '62', 'target': '63', 'type': 'activation'}}, {'data': {'source': '62', 'target': '69', 'type': 'activation'}}, {'data': {'source': '53', 'target': '62', 'type': 'activation'}}, {'data': {'source': '52', 'target': '63', 'type': 'activation'}}, {'data': {'source': '53', 'target': '63', 'type': 'activation'}}, {'data': {'source': '58', 'target': '25', 'type': 'activation'}}, {'data': {'source': '58', 'target': '69', 'type': 'inhibition'}}, {'data': {'source': '30', 'target': '28', 'type': 'activation'}}, {'data': {'source': '24', 'target': '25', 'type': 'activation'}}, {'data': {'source': '23', 'target': '24', 'type': 'activation'}}, {'data': {'source': '23', 'target': '22', 'type': 'activation'}}, {'data': {'source': '21', 'target': '20', 'type': 'activation'}}, {'data': {'source': '17', 'target': '16', 'type': 'activation'}}, {'data': {'source': '17', 'target': '15', 'type': 'activation'}}, {'data': {'source': '17', 'target': '14', 'type': 'activation'}}, {'data': {'source': '15', 'target': '13', 'type': 'activation'}}, {'data': {'source': '63', 'target': '41', 'type': 'activation'}}, {'data': {'source': '25', 'target': '29', 'type': 'activation'}}, {'data': {'source': '26', 'target': '29', 'type': 'activation'}}, {'data': {'source': '25', 'target': '26', 'type': 'activation'}}, {'data': {'source': '19', 'target': '18', 'type': 'activation'}}, {'data': {'source': '41', 'target': '36', 'type': 'activation'}}, {'data': {'source': '41', 'target': '35', 'type': 'activation'}}, {'data': {'source': '41', 'target': '34', 'type': 'activation'}}, {'data': {'source': '41', 'target': '33', 'type': 'activation'}}, {'data': {'source': '41', 'target': '32', 'type': 'activation'}}, {'data': {'source': '41', 'target': '31', 'type': 'activation'}}, {'data': {'source': '66', 'target': '63', 'type': 'inhibition'}}, {'data': {'source': '80', 'target': '76', 'type': 'activation'}}, {'data': {'source': '81', 'target': '76', 'type': 'activation'}}, {'data': {'source': '81', 'target': '77', 'type': 'activation'}}, {'data': {'source': '81', 'target': '69', 'type': 'activation'}}, {'data': {'source': '83', 'target': '76', 'type': 'inhibition'}}, {'data': {'source': '84', 'target': '76', 'type': 'inhibition'}}, {'data': {'source': '85', 'target': '25', 'type': 'activation'}}, {'data': {'source': '86', 'target': '80', 'type': 'inhibition'}}, {'data': {'source': '57', 'target': '55', 'type': 'activation'}}, {'data': {'source': '55', 'target': '54', 'type': 'activation'}}, {'data': {'source': '54', 'target': '53', 'type': 'activation'}}, {'data': {'source': '56', 'target': '54', 'type': 'activation'}}, {'data': {'source': '57', 'target': '63', 'type': 'activation'}}, {'data': {'source': '28', 'target': '27', 'type': 'activation'}}, {'data': {'source': '52', 'target': '51', 'type': 'activation'}}, {'data': {'source': '51', 'target': '50', 'type': 'activation'}}, {'data': {'source': '50', 'target': '49', 'type': 'activation'}}]},
});

var options = {
  name: 'cose',

  // Called on `layoutready`
  ready: function(){},

  // Called on `layoutstop`
  stop: function(){},

  // Whether to animate while running the layout
  // true : Animate continuously as the layout is running
  // false : Just show the end result
  // 'end' : Animate with the end result, from the initial positions to the end positions
  animate: true,

  // Easing of the animation for animate:'end'
  animationEasing: undefined,

  // The duration of the animation for animate:'end'
  animationDuration: undefined,

  // A function that determines whether the node should be animated
  // All nodes animated by default on animate enabled
  // Non-animated nodes are positioned immediately when the layout starts
  animateFilter: function ( node, i ){ return true; },


  // The layout animates only after this many milliseconds for animate:true
  // (prevents flashing on fast runs)
  animationThreshold: 250,

  // Number of iterations between consecutive screen positions update
  // (0 -> only updated on the end)
  refresh: 20,

  // Whether to fit the network view after when done
  fit: true,

  // Padding on fit
  padding: 30,

  // Constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
  boundingBox: undefined,

  // Excludes the label when calculating node bounding boxes for the layout algorithm
  nodeDimensionsIncludeLabels: false,

  // Randomize the initial positions of the nodes (true) or use existing positions (false)
  randomize: false,

  // Extra spacing between components in non-compound graphs
  componentSpacing: 40,

  // Node repulsion (non overlapping) multiplier
  nodeRepulsion: function( node ){ return 2048; },

  // Node repulsion (overlapping) multiplier
  nodeOverlap: 4,

  // Ideal edge (non nested) length
  idealEdgeLength: function( edge ){ return 32; },

  // Divisor to compute edge forces
  edgeElasticity: function( edge ){ return 32; },

  // Nesting factor (multiplier) to compute ideal edge length for nested edges
  nestingFactor: 1.2,

  // Gravity force (constant)
  gravity: 1,

  // Maximum number of iterations to perform
  numIter: 1000,

  // Initial temperature (maximum node displacement)
  initialTemp: 1000,

  // Cooling factor (how the temperature is reduced between consecutive iterations
  coolingFactor: 0.99,

  // Lower temperature threshold (below this point the layout will end)
  minTemp: 1.0,

  // Pass a reference to weaver to use threads for calculations
  weaver: false
};

layout = cy.layout( options );

layout.run();

cy.filter('node[type = "mutation"]').style('background-color', '#6495ED');
cy.filter('node[type = "non-mutation"]').style('background-color', '#A6A6A6');
cy.filter('edge[type = "inhibition"]').style('target-arrow-shape', 'tee');
cy.nodes('[label="seed"]').style('background-color', '#FF0000');
cy.on('click','node',function (evt) {
    // document.getElementById("eg").innerText = evt.target.attr('type');
    document.getElementById("eg").innerText = "click";
});
