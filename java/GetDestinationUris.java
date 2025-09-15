public class GetDestinationUris {
    public static void main(String[] args) throws Exception {
        String trunkSid = System.getenv("TRUNK_SID");
        if (trunkSid == null || trunkSid.isEmpty()) {
            System.err.println("Error: TRUNK_SID environment variable is required");
            System.exit(1);
        }

        System.out.printf("Getting destination URIs for trunk %s...%n", trunkSid);
        String result = _Client.get(String.format("/trunks/%s/destination-uris", trunkSid));
        System.out.println("Destination URIs retrieved successfully!");
    }
} 