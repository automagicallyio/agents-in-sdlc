from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Publisher(BaseModel):
    """
    Publisher model representing a game publisher in the crowdfunding platform.
    
    Attributes:
        id: Primary key
        name: Name of the publisher (unique)
        description: Detailed description of the publisher
        games: Relationship to Game models published by this publisher
    """
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # One-to-many relationship: one publisher has many games
    games = relationship("Game", back_populates="publisher")

    @validates('name')
    def validate_name(self, key, name):
        """
        Validate the publisher name field.
        
        Args:
            key: The field name being validated
            name: The name value to validate
            
        Returns:
            The validated name
        """
        return self.validate_string_length('Publisher name', name, min_length=2)

    @validates('description')
    def validate_description(self, key, description):
        """
        Validate the publisher description field.
        
        Args:
            key: The field name being validated
            description: The description value to validate
            
        Returns:
            The validated description
        """
        return self.validate_string_length('Description', description, min_length=10, allow_none=True)

    def __repr__(self):
        """
        Return string representation of the Publisher model.
        
        Returns:
            String representation including publisher name
        """
        return f'<Publisher {self.name}>'

    def to_dict(self):
        """
        Convert the Publisher model to a dictionary.
        
        Returns:
            Dictionary containing publisher data including game count
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'game_count': len(self.games) if self.games else 0
        }