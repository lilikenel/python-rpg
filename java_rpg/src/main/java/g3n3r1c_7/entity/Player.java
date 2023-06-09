package g3n3r1c_7.entity;

import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;

import g3n3r1c_7.GamePanel;
import g3n3r1c_7.KeyHandler;

public class Player extends Entity {
    
    GamePanel gamePanel;
    KeyHandler keyHandler;

    BufferedImage up1, up2, down1, down2, left1, left2, right1, right2;

    public Player(GamePanel gamePanel, KeyHandler keyHandler) {

        this.gamePanel = gamePanel;
        this.keyHandler = keyHandler;
        setDefaultValues();
        getPlayerImage();
    }

    public void setDefaultValues() {

        x = (gamePanel.screenWidth/2) - (gamePanel.tileSize/2);
        y = gamePanel.screenHeight/2 - (gamePanel.tileSize/2);
        speed = 3;
        direction = DIRECTION.DOWN;
    }

    public void getPlayerImage() {

        try {

            up1 = ImageIO.read(new File("java_rpg/res/hero/hero_back_01.png"));
            up2 = ImageIO.read(new File("java_rpg/res/hero/hero_back_02.png"));
            down1 = ImageIO.read(new File("java_rpg/res/hero/hero_front_01.png"));
            down2 = ImageIO.read(new File("java_rpg/res/hero/hero_front_02.png"));
            left1 = ImageIO.read(new File("java_rpg/res/hero/hero_left_01.png"));
            left2 = ImageIO.read(new File("java_rpg/res/hero/hero_left_02.png"));
            right1 = ImageIO.read(new File("java_rpg/res/hero/hero_right_01.png"));
            right2 = ImageIO.read(new File("java_rpg/res/hero/hero_right_02.png"));

        } catch(IOException e) {
            e.printStackTrace();
        }
    }

    public void update() {

        if(keyHandler.upPressed == true) {
            direction = DIRECTION.UP;
            y -= speed;
        }
        else if(keyHandler.downPressed == true) {
            direction = DIRECTION.DOWN;
            y += speed;
        }
        else if(keyHandler.leftPressed == true) {
            direction = DIRECTION.LEFT;
            x -= speed;
        }
        else if(keyHandler.rightPressed == true) {
            direction = DIRECTION.RIGHT;
            x += speed;
        }

        if (keyHandler.upPressed == true ||
            keyHandler.rightPressed == true||
                keyHandler.downPressed == true ||
                    keyHandler.leftPressed == true) {
            spriteCounter++;
        }

        if (spriteCounter > 13) {
            if (spriteNum == 1) {
                spriteNum = 2;
            }
            else if (spriteNum == 2) {
                spriteNum = 1;
            }
            spriteCounter = 0;
        }
    }

    public void draw(Graphics2D graphics2D) {

        // graphics2D.setColor(Color.white);
        // graphics2D.fillRect(x, y, gamePanel.tileSize, gamePanel.tileSize);

        BufferedImage image = null;

        switch(direction) {
            case UP:
                if (spriteNum == 1) {
                    image = up1;
                }
                if (spriteNum == 2) {
                    image = up2;
                }
                break;
            case RIGHT:
                if (spriteNum == 1) {
                    image = right1;
                }
                if (spriteNum == 2) {
                    image = right2;
                }
                break;
            case DOWN:
                if (spriteNum == 1) {
                    image = down1;
                }
                if (spriteNum == 2) {
                    image = down2;
                }
                break;
            case LEFT:
                if (spriteNum == 1) {
                    image = left1;
                }
                if (spriteNum == 2) {
                    image = left2;
                }
                break;
        }

        graphics2D.drawImage(image, x, y, gamePanel.tileSize, gamePanel.tileSize, null);
    }
}
