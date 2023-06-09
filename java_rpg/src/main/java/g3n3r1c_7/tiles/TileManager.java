package g3n3r1c_7.tiles;

import java.awt.Graphics2D;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;

import g3n3r1c_7.GamePanel;

public class TileManager {
    
    GamePanel gamePanel;
    Tile[] tile;

    public TileManager(GamePanel gamePanel) {

        this.gamePanel = gamePanel;
        tile = new Tile[1];
        getTileImage();
    }

    public void getTileImage() {

        try {
            tile[0] = new Tile();
            tile[0].image = ImageIO.read(new File("java_rpg/res/tiles/tile_01.png"));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void draw(Graphics2D graphics2d) {

        int col = 0;
        int row = 0;
        int x = 0;
        int y = 0;

        while(col < gamePanel.maxScreenCol && row < gamePanel.maxScreenRow) {

            graphics2d.drawImage(tile[0].image, x, y, gamePanel.tileSize, gamePanel.tileSize, null);

            col++;
            x += gamePanel.tileSize;

            if (col == gamePanel.maxScreenCol) {
                col = 0;
                x = 0;
                row++;
                y += gamePanel.tileSize;
            }
        }

    }
}
