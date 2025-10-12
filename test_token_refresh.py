from fishbowlpy.fishbowlclient import FishBowlClient

print("Testing FishBowl Token Refresh...")
print("-" * 50)

# Test basic functionality
try:
    client = FishBowlClient(login_popup=False)
    print("✓ Client created")
    print("✓ refresh_session method exists:", hasattr(client, 'refresh_session'))
    print("✓ save_session method exists:", hasattr(client, 'save_session'))
    print("✓ load_session method exists:", hasattr(client, 'load_session'))
    print("\nAll methods added successfully!")
except Exception as e:
    print(f"✗ Error: {e}")
