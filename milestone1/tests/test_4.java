public class SwitchTest {
    public void handleRequest(Request request) {
        switch (request.getType()) {
            case GET:
                switch (request.getResource()) {
                    case "users":
                        // Handle getting user data
                        break;
                    case "posts":
                        // Handle getting post data
                        break;
                    case "comments":
                        // Handle getting comment data
                        break;
                    default:
                        throw new IllegalArgumentException("Invalid resource: " + request.getResource());
                }
                break;
            case POST:
                switch (request.getResource()) {
                    case "users":
                        // Handle creating a new user
                        break;
                    case "posts":
                        // Handle creating a new post
                        break;
                    case "comments":
                        // Handle creating a new comment
                        break;
                    default:
                        throw new IllegalArgumentException("Invalid resource: " + request.getResource());
                }
                break;
            case PUT:
                switch (request.getResource()) {
                    case "users":
                        // Handle updating user data
                        break;
                    case "posts":
                        // Handle updating post data
                        break;
                    case "comments":
                        // Handle updating comment data
                        break;
                    default:
                        throw new IllegalArgumentException("Invalid resource: " + request.getResource());
                }
                break;
            case DELETE:
                switch (request.getResource()) {
                    case "users":
                        // Handle deleting a user
                        break;
                    case "posts":
                        // Handle deleting a post
                        break;
                    case "comments":
                        // Handle deleting a comment
                        break;
                    default:
                        throw new IllegalArgumentException("Invalid resource: " + request.getResource());
                }
                break;
            default:
                throw new IllegalArgumentException("Invalid request type: " + request.getType());
        }
    }

}