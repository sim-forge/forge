<script>
  import { onMount } from 'svelte';
  import Button from '$lib/components/Button.svelte';
  import Card from '$lib/components/Card.svelte';
  import Input from '$lib/components/Input.svelte';
  import Textarea from '$lib/components/Textarea.svelte';
  import Select from '$lib/components/Select.svelte';
  import Switch from '$lib/components/Switch.svelte';
  import Badge from '$lib/components/Badge.svelte';
  import Alert from '$lib/components/Alert.svelte';
  import Tabs from '$lib/components/Tabs.svelte';
  import Modal from '$lib/components/Modal.svelte';
  import Tooltip from '$lib/components/Tooltip.svelte';
  import Dropdown from '$lib/components/Dropdown.svelte';
  import Progress from '$lib/components/Progress.svelte';
  import Skeleton from '$lib/components/Skeleton.svelte';
  import Avatar from '$lib/components/Avatar.svelte';
  import Accordion from '$lib/components/Accordion.svelte';
  import Pagination from '$lib/components/Pagination.svelte';
  import Breadcrumb from '$lib/components/Breadcrumb.svelte';
  import Slider from '$lib/components/Slider.svelte';
  import ColorPicker from '$lib/components/ColorPicker.svelte';
  
  // Local state
  let modalOpen = false;
  let sliderValue = 50;
  let switchValue = false;
  let colorValue = '#1890ff';
  let selectedTab = 'buttons';
  
  // Sample data
  const tabs = [
    { id: 'buttons', label: 'Buttons' },
    { id: 'inputs', label: 'Inputs' },
    { id: 'feedback', label: 'Feedback' },
    { id: 'navigation', label: 'Navigation' },
    { id: 'data', label: 'Data Display' }
  ];
  
  const accordionItems = [
    { 
      id: 'item1', 
      title: 'What is SimForge?', 
      content: 'SimForge is a local-first, production-grade synthetic cognition tool. It enables users to generate, edit, and visualize structured data — such as belief-action sequences — using a smart table interface powered by LLMs.'
    },
    { 
      id: 'item2', 
      title: 'How does it work?', 
      content: 'SimForge uses a combination of local and remote LLMs to generate and validate structured data. It provides a smart table interface for editing and visualizing this data, with support for forking, batch generation, and modular prompt authoring.'
    },
    { 
      id: 'item3', 
      title: 'Is it open source?', 
      content: 'Yes, SimForge is open source and available on GitHub. You can contribute to the project by submitting pull requests or reporting issues.'
    }
  ];
  
  const breadcrumbItems = [
    { label: 'Home', href: '/' },
    { label: 'Components', href: '/components' },
    { label: 'UI Library', active: true }
  ];
  
  const dropdownItems = [
    { label: 'Profile', icon: '👤' },
    { label: 'Settings', icon: '⚙️' },
    { type: 'divider' },
    { label: 'Logout', icon: '🚪', danger: true }
  ];
  
  // Initialize component
  onMount(() => {
    // Component initialization
  });
</script>

<svelte:head>
  <title>SimForge UI Components</title>
</svelte:head>

<div class="container mx-auto px-4 py-8">
  <h1 class="text-3xl font-bold mb-8">SimForge UI Components</h1>
  
  <Tabs 
    {tabs} 
    bind:activeTab={selectedTab} 
    variant="underline" 
    fullWidth={true}
  />
  
  {#if selectedTab === 'buttons'}
    <div class="mt-8">
      <h2 class="text-2xl font-semibold mb-4">Buttons</h2>
      
      <Card class="p-6 mb-8">
        <h3 class="text-lg font-medium mb-4">Button Variants</h3>
        <div class="flex flex-wrap gap-4">
          <Button>Default</Button>
          <Button variant="primary">Primary</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="success">Success</Button>
          <Button variant="warning">Warning</Button>
          <Button variant="error">Error</Button>
          <Button variant="outline">Outline</Button>
          <Button variant="ghost">Ghost</Button>
          <Button variant="link">Link</Button>
        </div>
      </Card>
      
      <Card class="p-6 mb-8">
        <h3 class="text-lg font-medium mb-4">Button Sizes</h3>
        <div class="flex flex-wrap items-center gap-4">
          <Button size="xs">Extra Small</Button>
          <Button size="sm">Small</Button>
          <Button size="md">Medium</Button>
          <Button size="lg">Large</Button>
          <Button size="xl">Extra Large</Button>
        </div>
      </Card>
      
      <Card class="p-6 mb-8">
        <h3 class="text-lg font-medium mb-4">Button States</h3>
        <div class="flex flex-wrap gap-4">
          <Button>Normal</Button>
          <Button loading={true}>Loading</Button>
          <Button disabled>Disabled</Button>
          <Button iconLeft="🔍">With Icon</Button>
          <Button iconRight="→">Icon Right</Button>
          <Button fullWidth>Full Width</Button>
        </div>
      </Card>
      
      <Card class="p-6">
        <h3 class="text-lg font-medium mb-4">Button Groups</h3>
        <div class="flex flex-wrap gap-4">
          <div class="inline-flex rounded-md shadow-sm">
            <Button class="rounded-r-none">Left</Button>
            <Button class="rounded-none border-l-0 border-r-0">Middle</Button>
            <Button class="rounded-l-none">Right</Button>
          </div>
        </div>
      </Card>
    </div>
  {/if}
  
  {#if selectedTab === 'inputs'}
    <div class="mt-8">
      <h2 class="text-2xl font-semibold mb-4">Form Inputs</h2>
      
      <Card class="p-6 mb-8">
        <h3 class="text-lg font-medium mb-4">Text Inputs</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Input 
            label="Username" 
            placeholder="Enter your username" 
            helperText="Your unique identifier"
          />
          
          <Input 
            label="Email" 
            type="email" 
            placeholder="example@email.com" 
            required
          />
          
          <Input 
            label="Password" 
            type="password" 
            placeholder="Enter your password" 
            error="Password must be at least 8 characters"
          />
          
          <Input 
            label="Disabled Input" 
            value="Cannot be changed" 
            disabled
          />
          
          <Input 
            label="With Icon" 
            placeholder="Search..." 
            iconLeft="🔍"
          />
          
          <Input 
            label="With Button" 
            placeholder="Verification code" 
            buttonRight="Verify"
          />
        </div>
      </Card>
      
      <Card class="p-6 mb-8">
        <h3 class="text-lg font-medium mb-4">Select & Textarea</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Select 
            label="Country" 
            options={[
              { value: 'us', label: 'United States' },
              { value: 'ca', label: 'Canada' },
              { value: 'mx', label: 'Mexico' },
              { value: 'uk', label: 'United Kingdom' },
              { value: 'fr', label: 'France' },
              { value: 'de', label: 'Germany' },
              { value: 'jp', label: 'Japan' }
            ]}
            placeholder="Select a country"
          />
          
          <Select 
            label="Interests" 
            options={[
              { value: 'tech', label: 'Technology' },
              { value: 'art', label: 'Art & Design' },
              { value: 'science', label: 'Science' },
              { value: 'sports', label: 'Sports' },
              { value: 'music', label: 'Music' },
              { value: 'travel', label: 'Travel' }
            ]}
            placeholder="Select your interests"
            multiple
            searchable
          />
          
          <Textarea 
            label="Bio" 
            placeholder="Tell us about yourself" 
            rows={4}
            maxLength={200}
            showCount
          />
          
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-1">
              Toggle Switch
            </label>
            <div class="space-y-4">
              <Switch 
                label="Enable notifications" 
                bind:checked={switchValue}
              />
              
              <Switch 
                label="Dark mode" 
                labelPosition="left"
                checked={true}
              />
              
              <Switch 
                label="Disabled option" 
                disabled
              />
            </div>
          </div>
        </div>
      </Card>
      
      <Card class="p-6 mb-8">
        <h3 class="text-lg font-medium mb-4">Sliders & Color Pickers</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-1">
              Volume
            </label>
            <Slider 
              bind:value={sliderValue} 
              min={0} 
              max={100} 
              step={1}
              showValue
              showTicks
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-1">
              Price Range
            </label>
            <Slider 
              range 
              rangeValue={[20, 80]} 
              min={0} 
              max={100}
              showValue
              valuePosition="bottom"
            />
          </div>
          
          <ColorPicker 
            label="Theme Color" 
            bind:value={colorValue}
            showAlpha
          />
        </div>
      </Card>
    </div>
  {/if}
  
  {#if selectedTab === 'feedback'}
    <div class="mt-8">
      <h2 class="text-2xl font-semibold mb-4">Feedback Components</h2>
      
      <Card class="p-6 mb-8">
        <h3 class="text-lg font-medium mb-4">Alerts</h3>
        <div class="space-y-4">
          <Alert 
            type="info" 
            title="Information" 
            message="This is an informational message."
            dismissible
          />
          
          <Alert 
            type="success" 
            title="Success" 
            message="Your changes have been saved successfully."
            dismissible
          />
          
          <Alert 
            type="warning" 
            title="Warning" 
            message="This action cannot be undone."
            dismissible
          />
          
          <Alert 
            type="error" 
            title="Error" 
            message="An error occurred while processing your request."
            dismissible
          />
        </div>
      </Card>
      
      <Card class="p-6 mb-8">
        <h3 class="text-lg font-medium mb-4">Progress & Loading</h3>
        <div class="space-y-6">
          <Progress 
            value={30} 
            max={100} 
            showLabel 
            labelPosition="right"
          />
          
          <Progress 
            value={60} 
            max={100} 
            color="success" 
            showLabel
            striped
          />
          
          <Progress 
            value={80} 
            max={100} 
            color="warning" 
            showLabel
            striped
            animated
          />
          
          <Progress 
            indeterminate 
            color="primary"
          />
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Skeleton variant="rectangle" height="100px" />
            <Skeleton variant="text" count={3} />
            <Skeleton variant="circle" width="80px" height="80px" />
          </div>
        </div>
      </Card>
      
      <Card class="p-6 mb-8">
        <h3 class="text-lg font-medium mb-4">Modals & Tooltips</h3>
        <div class="flex flex-wrap gap-4">
          <Button on:click={() => modalOpen = true}>
            Open Modal
          </Button>
          
          <Tooltip content="This is a tooltip">
            <Button variant="outline">Hover Me</Button>
          </Tooltip>
        </div>
      </Card>
      
      <Card class="p-6">
        <h3 class="text-lg font-medium mb-4">Badges</h3>
        <div class="flex flex-wrap gap-4">
          <Badge>Default</Badge>
          <Badge variant="primary">Primary</Badge>
          <Badge variant="success">Success</Badge>
          <Badge variant="warning">Warning</Badge>
          <Badge variant="error">Error</Badge>
          <Badge variant="primary" outline>Outline</Badge>
          <Badge variant="primary" rounded>Rounded</Badge>
          <Badge variant="primary" removable>Removable</Badge>
        </div>
      </Card>
    </div>
  {/if}
  
  {#if selectedTab === 'navigation'}
    <div class="mt-8">
      <h2 class="text-2xl font-semibold mb-4">Navigation Components</h2>
      
      <Card class="p-6 mb-8">
        <h3 class="text-lg font-medium mb-4">Tabs</h3>
        <div class="space-y-8">
          <Tabs 
            tabs={[
              { id: 'tab1', label: 'Account' },
              { id: 'tab2', label: 'Password' },
              { id: 'tab3', label: 'Notifications' }
            ]} 
            activeTab="tab1"
            variant="default"
          />
          
          <Tabs 
            tabs={[
              { id: 'pill1', label: 'Overview', icon: '📊' },
              { id: 'pill2', label: 'Analytics', icon: '📈' },
              { id: 'pill3', label: 'Reports', icon: '📝' }
            ]} 
            activeTab="pill1"
            variant="pills"
          />
        </div>
      </Card>
      
      <Card class="p-6 mb-8">
        <h3 class="text-lg font-medium mb-4">Breadcrumbs & Pagination</h3>
        <div class="space-y-8">
          <Breadcrumb items={breadcrumbItems} />
          
          <Pagination 
            totalItems={100} 
            pageSize={10} 
            currentPage={3}
            showPageSize
          />
        </div>
      </Card>
      
      <Card class="p-6 mb-8">
        <h3 class="text-lg font-medium mb-4">Dropdowns & Accordions</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <Dropdown 
              items={dropdownItems}
              label="User Menu"
            />
          </div>
          
          <div>
            <Accordion 
              items={accordionItems}
              multiple={false}
              defaultOpen={['item1']}
            />
          </div>
        </div>
      </Card>
    </div>
  {/if}
  
  {#if selectedTab === 'data'}
    <div class="mt-8">
      <h2 class="text-2xl font-semibold mb-4">Data Display Components</h2>
      
      <Card class="p-6 mb-8">
        <h3 class="text-lg font-medium mb-4">Cards</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <div class="p-4">
              <h4 class="text-lg font-medium mb-2">Basic Card</h4>
              <p class="text-text-secondary">This is a basic card with some content.</p>
            </div>
          </Card>
          
          <Card>
            <img src="https://via.placeholder.com/300x150" alt="Placeholder" class="w-full h-40 object-cover" />
            <div class="p-4">
              <h4 class="text-lg font-medium mb-2">Card with Image</h4>
              <p class="text-text-secondary">This card has an image at the top.</p>
            </div>
          </Card>
          
          <Card>
            <div class="p-4">
              <h4 class="text-lg font-medium mb-2">Card with Actions</h4>
              <p class="text-text-secondary">This card has action buttons.</p>
            </div>
            <div class="border-t border-border-light p-4 flex justify-end space-x-2">
              <Button variant="ghost" size="sm">Cancel</Button>
              <Button variant="primary" size="sm">Save</Button>
            </div>
          </Card>
        </div>
      </Card>
      
      <Card class="p-6 mb-8">
        <h3 class="text-lg font-medium mb-4">Avatars</h3>
        <div class="flex flex-wrap gap-6">
          <Avatar 
            name="John Doe" 
            size="xs"
          />
          
          <Avatar 
            name="Jane Smith" 
            size="sm"
            backgroundColor="#1890ff"
            textColor="white"
          />
          
          <Avatar 
            name="Alex Johnson" 
            size="md"
            shape="square"
          />
          
          <Avatar 
            name="Sam Wilson" 
            size="lg"
            status="online"
          />
          
          <Avatar 
            name="Taylor Swift" 
            size="xl"
            src="https://via.placeholder.com/150"
            border
          />
        </div>
      </Card>
    </div>
  {/if}
</div>

<Modal 
  bind:open={modalOpen}
  title="Example Modal"
  size="md"
>
  <div class="p-4">
    <p class="mb-4">This is an example modal dialog. You can put any content here.</p>
    
    <Input 
      label="Your Name" 
      placeholder="Enter your name"
    />
  </div>
  
  <div slot="footer" class="px-6 py-4 bg-bg-secondary border-t border-border-light flex justify-end space-x-2">
    <Button variant="ghost" on:click={() => modalOpen = false}>Cancel</Button>
    <Button variant="primary" on:click={() => modalOpen = false}>Save</Button>
  </div>
</Modal>