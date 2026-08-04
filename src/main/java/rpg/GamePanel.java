package rpg;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;

import javax.swing.JPanel;

import rpg.entity.Player;
import rpg.tiles.TileManager;

public class GamePanel extends JPanel implements Runnable {
	
	final int originalTileSize = 16;
	final int scale = 3;
	public final int tileSize = originalTileSize * scale; //48x48 px

	public final int maxScreenCol = 16;
	public final int maxScreenRow = 12;

	public final int screenWidth = tileSize * maxScreenCol; //786 px
	public final int screenHeight = tileSize * maxScreenRow; //574 px

	Thread gameThread;
	KeyHandler keyHandler = new KeyHandler();
	TileManager tileManager = new TileManager(this);
	Player player = new Player(this, keyHandler);

	int FPS = 60;

	public GamePanel() {

		this.setPreferredSize(new Dimension(screenWidth, screenHeight));
		this.setBackground(Color.black);
		this.setDoubleBuffered(true); //better rendering performance
		this.addKeyListener(keyHandler);
		this.setFocusable(true);
	}

	public void startGameThread() {

		gameThread = new Thread(this);
		gameThread.start();
	}

	/*
	* the main game loop
	*/
	@Override
	public void run() {

		double drawInterval = 1000000000 / FPS;
		double delta = 0;
		long lastTime = System.nanoTime();
		long currentTime;
	
		while (gameThread != null) {

			currentTime = System.nanoTime();
			delta += (currentTime - lastTime) / drawInterval;
			lastTime = currentTime;

			if (delta >= 1) {
				update();
				repaint(); //calls paintComponent()
				delta--;
			}
			
		}        
	}

	public void update() {

		player.update();
	}

	/*
	* Essentially the paintbrush we use to draw on window in Main.java
	*/
	public void paintComponent(Graphics graphics) {

		super.paintComponent(graphics);

		Graphics2D graphics2D = (Graphics2D) graphics;

		tileManager.draw(graphics2D);
		player.draw(graphics2D);

		graphics2D.dispose();
	}
}
