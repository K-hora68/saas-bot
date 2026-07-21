from app.models.messages import Message
from app.extensions import db


class Message_Repo:

    def create(
        self,
        session_id: int,
        sender: str,
        message_type: str,
        content: str
    ) -> Message:

        message = Message(
            session_id=session_id,
            sender=sender,
            message_type=message_type,
            content=content
        )

        db.session.add(message)
        db.session.commit()

        return message

    def get_by_id(
        self,
        message_id: int
    ) -> Message | None:

        return Message.query.get(message_id)

    def get_history(
        self,
        session_id: int
    ) -> list[Message]:

        return (
            Message.query
            .filter_by(session_id=session_id)
            .order_by(Message.created_at.asc())
            .all()
        )

    def get_last_message(
        self,
        session_id: int
    ) -> Message | None:

        return (
            Message.query
            .filter_by(session_id=session_id)
            .order_by(Message.created_at.desc())
            .first()
        )

    def delete(
        self,
        message: Message
    ) -> None:

        db.session.delete(message)
        db.session.commit()

    def delete_session_messages(
        self,
        session_id: int
    ) -> None:

        (
            Message.query
            .filter_by(session_id=session_id)
            .delete()
        )

        db.session.commit()
    