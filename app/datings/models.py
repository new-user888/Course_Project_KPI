from app import db


class Invitation(db.Model):
    __tablename__ = 'invitations'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    state = db.Column(db.String(8))

    sender = db.relationship("User", foreign_keys=[sender_id])
    receiver = db.relationship("User", foreign_keys=[receiver_id])

    @classmethod
    def create_invitation(cls, sender_id, receiver_id, state):
        invitation = cls(sender_id=sender_id,
                         receiver_id=receiver_id,
                         state=state,
                         )
        db.session.add(invitation)
        db.session.commit()
        return invitation
