

from database import RegisterDetails, User_Post


class UserAuthPolicy:
    
    @staticmethod
    def can_access_post_data(current_user: RegisterDetails, post: User_Post) :
        
        if current_user.role == "admin":
            return True
        
        if current_user.role == "user":
            return post.owner_id == current_user.id