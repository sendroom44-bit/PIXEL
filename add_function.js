const fs = require('fs');

const p = 'games/templates/games/prison_pacman2.html';
let s = fs.readFileSync(p, 'utf8');

const f = `
function getFreeCells(map) {
    const cells = [];

    for (let y = 0; y < SIZE; y++) {
        for (let x = 0; x < SIZE; x++) {
            if (map[y] && map[y][x] !== '#') {
                cells.push({x: x, y: y});
            }
        }
    }

    return cells;
}
`;

s = s.replace('function prepareMap', f + '\\nfunction prepareMap');
fs.writeFileSync(p, s, 'utf8');