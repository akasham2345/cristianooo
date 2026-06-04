import random
import time
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional

class Season(Enum):
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"
    WINTER = "winter"

class Weather(Enum):
    SUNNY = "sunny"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    STORMY = "stormy"

@dataclass
class Fish:
    name: str
    rarity: str  # common, uncommon, rare, legendary
    difficulty: int  # 1-10
    weight_range: tuple  # (min, max) in pounds
    behavior: str  # aggressive, cautious, playful, lazy
    best_season: Season
    description: str
    personality: str

class FishingGame:
    """An original fishing game with personality, strategy, and progression."""
    
    FISH_CATALOG = [
        Fish("Bass", "common", 3, (2, 8), "aggressive", Season.SUMMER, 
             "A feisty fighter that loves warm waters", "Aggressive and bold"),
        Fish("Trout", "uncommon", 4, (1, 5), "cautious", Season.SPRING,
             "A careful fish that hides in cold streams", "Shy and intelligent"),
        Fish("Salmon", "rare", 7, (15, 30), "playful", Season.FALL,
             "Leaps majestically upstream during migration", "Acrobatic and determined"),
        Fish("Catfish", "uncommon", 5, (5, 25), "lazy", Season.SUMMER,
             "A bottom-dweller that prefers muddy waters", "Grumpy but patient"),
        Fish("Pike", "rare", 8, (10, 20), "aggressive", Season.FALL,
             "The apex predator of freshwater", "Fierce and calculating"),
        Fish("Goldfish", "common", 1, (0.5, 2), "playful", Season.SPRING,
             "A decorative fish that escaped from a pond", "Curious and friendly"),
        Fish("Piranha", "legendary", 9, (2, 5), "aggressive", Season.SUMMER,
             "A legendary creature rumored to lurk in deep waters", "Dangerous and unpredictable"),
        Fish("Koi", "legendary", 6, (20, 50), "lazy", Season.SPRING,
             "An ancient, wise fish covered in beautiful patterns", "Calm and meditative"),
    ]
    
    def __init__(self):
        self.player_name = ""
        self.skill_level = 1
        self.experience = 0
        self.level_threshold = 100
        self.inventory: List[Fish] = []
        self.total_catch_weight = 0
        self.fish_caught: Dict[str, int] = {}
        self.current_season = Season.SUMMER
        self.current_weather = Weather.SUNNY
        self.money = 100
        self.gear_quality = 1  # 1-5 star rating
        self.fishing_streak = 0
        self.achievements: List[str] = []
        
    def start_game(self, player_name: str):
        """Initialize the game with player name."""
        self.player_name = player_name
        print(f"\n🎣 Welcome, {player_name}! You are starting your fishing journey.")
        print(f"Skill Level: {self.skill_level} | Money: ${self.money} | Gear Quality: {'⭐' * self.gear_quality}")
        print("\nLet's set the scene for your adventure...")
        self.set_conditions()
        
    def set_conditions(self):
        """Randomly set weather and season conditions."""
        self.current_season = random.choice(list(Season))
        self.current_weather = random.choice(list(Weather))
        self._display_conditions()
        
    def _display_conditions(self):
        """Show current fishing conditions."""
        weather_emoji = {
            Weather.SUNNY: "☀️",
            Weather.CLOUDY: "☁️",
            Weather.RAINY: "🌧️",
            Weather.STORMY: "⛈️"
        }
        season_emoji = {
            Season.SPRING: "🌸",
            Season.SUMMER: "☀️",
            Season.FALL: "🍂",
            Season.WINTER: "❄️"
        }
        print(f"\n{season_emoji.get(self.current_season, '')} Season: {self.current_season.value.upper()}")
        print(f"{weather_emoji.get(self.current_weather, '')} Weather: {self.current_weather.value.upper()}")
        
    def fish(self) -> Optional[Fish]:
        """Attempt to catch a fish with skill-based mechanics."""
        print("\n🎣 You cast your line into the water...")
        time.sleep(1)
        
        available_fish = [f for f in self.FISH_CATALOG if f.best_season == self.current_season]
        
        if not available_fish:
            available_fish = self.FISH_CATALOG
        
        # Calculate catch probability based on multiple factors
        weather_bonus = {
            Weather.SUNNY: 0.8,
            Weather.CLOUDY: 1.0,
            Weather.RAINY: 1.1,
            Weather.STORMY: 0.5
        }
        
        catch_chance = (self.skill_level / 10) * weather_bonus[self.current_weather]
        catch_chance = min(catch_chance, 0.95)
        
        if random.random() > catch_chance:
            print("❌ The fish got away! Keep trying...")
            return None
        
        # Select a fish with rarity weighting
        selected_fish = random.choices(available_fish, 
                                      weights=[self._rarity_weight(f.rarity) for f in available_fish])[0]
        
        # Mini-game: Quick reaction test
        if not self._reaction_minigame(selected_fish):
            print(f"⚠️ A {selected_fish.name} approached but you didn't react in time!")
            return None
        
        # Calculate final fish stats
        weight = random.uniform(selected_fish.weight_range[0], selected_fish.weight_range[1])
        
        print(f"\n✨ You caught a {selected_fish.name}!")
        print(f"   Weight: {weight:.1f} lbs | Rarity: {selected_fish.rarity.upper()}")
        print(f"   '{selected_fish.personality}'")
        
        self._update_stats(selected_fish, weight)
        return selected_fish
        
    def _reaction_minigame(self, fish: Fish) -> bool:
        """Quick reaction-time mini-game."""
        difficulty_delay = fish.difficulty / 10
        print(f"\n⚡ React now! [Press Y]")
        time.sleep(difficulty_delay)
        # Simulated player input (in real game, use input())
        return random.random() > (fish.difficulty / 20)
        
    def _rarity_weight(self, rarity: str) -> float:
        """Return weight probability for rarity."""
        weights = {"common": 50, "uncommon": 30, "rare": 15, "legendary": 5}
        return weights.get(rarity, 10)
        
    def _update_stats(self, fish: Fish, weight: float):
        """Update player stats after catching a fish."""
        self.inventory.append(fish)
        self.total_catch_weight += weight
        self.fish_caught[fish.name] = self.fish_caught.get(fish.name, 0) + 1
        self.fishing_streak += 1
        
        # Experience and money
        xp_gain = (fish.difficulty * 10) + (weight * 2)
        money_gain = int(fish.difficulty * 5 * (1 if fish.rarity == "common" else 2))
        
        self.experience += xp_gain
        self.money += money_gain
        
        print(f"   +{int(xp_gain)} XP | +${money_gain}")
        
        self._check_level_up()
        self._check_achievements()
        
    def _check_level_up(self):
        """Check if player leveled up."""
        if self.experience >= self.level_threshold:
            self.skill_level += 1
            self.experience = 0
            self.level_threshold = int(self.level_threshold * 1.2)
            print(f"\n🎉 LEVEL UP! You are now level {self.skill_level}!")
            self.gear_quality = min(self.skill_level // 2 + 1, 5)
            
    def _check_achievements(self):
        """Check for achievement unlocks."""
        achievements = {
            "First Catch": len(self.inventory) == 1,
            "Tenacious Angler": self.fishing_streak >= 5,
            "Legendary Hunter": any(f.rarity == "legendary" for f in self.inventory),
            "Weight Champion": self.total_catch_weight > 100,
            "Collector": len(set(f.name for f in self.inventory)) >= 5,
        }
        
        for achievement, unlocked in achievements.items():
            if unlocked and achievement not in self.achievements:
                self.achievements.append(achievement)
                print(f"🏆 Achievement Unlocked: {achievement}!")
                
    def show_stats(self):
        """Display player statistics."""
        print("\n" + "="*50)
        print(f"📊 PLAYER STATS - {self.player_name.upper()}")
        print("="*50)
        print(f"Skill Level: {self.skill_level} ⭐{'⭐' * (self.skill_level - 1)}")
        print(f"Experience: {self.experience}/{self.level_threshold}")
        print(f"Money: ${self.money}")
        print(f"Gear Quality: {'⭐' * self.gear_quality}/⭐⭐⭐⭐⭐")
        print(f"Total Fish Caught: {len(self.inventory)}")
        print(f"Total Weight: {self.total_catch_weight:.1f} lbs")
        print(f"Current Streak: {self.fishing_streak}")
        
        if self.fish_caught:
            print("\n🐟 Fish Caught:")
            for fish_name, count in sorted(self.fish_caught.items(), key=lambda x: x[1], reverse=True):
                print(f"   {fish_name}: {count}")
                
        if self.achievements:
            print(f"\n🏆 Achievements ({len(self.achievements)}):")
            for achievement in self.achievements:
                print(f"   ✓ {achievement}")
                
    def show_fish_guide(self):
        """Display encyclopedia of all fish."""
        print("\n" + "="*50)
        print("📚 FISH ENCYCLOPEDIA")
        print("="*50)
        for fish in self.FISH_CATALOG:
            print(f"\n🐟 {fish.name}")
            print(f"   Rarity: {fish.rarity.upper()} | Difficulty: {fish.difficulty}/10")
            print(f"   Weight: {fish.weight_range[0]}-{fish.weight_range[1]} lbs")
            print(f"   Best Season: {fish.best_season.value.upper()}")
            print(f"   Behavior: {fish.behavior}")
            print(f"   Personality: {fish.personality}")
            print(f"   Description: {fish.description}")
            caught_count = self.fish_caught.get(fish.name, 0)
            print(f"   Caught: {caught_count} times")

def play_game():
    """Main game loop."""
    game = FishingGame()
    game.start_game("Angler")
    
    rounds = 0
    while rounds < 5:
        print("\n" + "-"*50)
        print(f"Fishing Session {rounds + 1}/5")
        print("-"*50)
        action = input("\n[F]ish, [S]tats, [G]uide, or [Q]uit? ").lower()
        
        if action == 'f':
            game.fish()
            rounds += 1
        elif action == 's':
            game.show_stats()
        elif action == 'g':
            game.show_fish_guide()
        elif action == 'q':
            break
            
    print("\n" + "="*50)
    print("🎣 Thanks for playing!")
    game.show_stats()
    print("="*50)

if __name__ == "__main__":
    play_game()