"""Houses agents without their own dedicated domain folder: Supplier Agent (import
orchestration), Market Agent (marketplace verification), Scoring Agent (0-100 confidence
score), Price Drop Agent, Bundle Agent. Profit, Risk, Trend, Alert, Listing, and Learning
agents live in their own top-level folders instead, since each owns substantial domain logic.

Agents communicate only through the database. Agents never call each other directly.
Not yet implemented.
"""
